#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

__author__ = "Idea Bosque"

from typing import Any, Dict

import humps
from silvaengine_utility import convert_decimal_to_number

from .error_handler import (
    ErrorCode,
    ValidationError,
    build_error_response,
    handle_errors,
    propagate_error_if_present,
    validate_not_empty,
)
from .graphql_backed_processor import GraphQLBackedProcessor

# Import status management
from .status_manager import (
    InstallmentStatus,
    QuoteOperationGuard,
    QuoteStatus,
    QuoteStatusTransitions,
    RequestOperationGuard,
)


class QuoteMixin(GraphQLBackedProcessor):
    """MCP tools for quote management."""

    # ==================== Private Helper Methods ====================

    # * Private helper method (not exposed as MCP tool)
    @handle_errors(operation_name="create quote")
    def _create_quote(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create new quote for RFQ request based on request items.
        Maps to GraphQL: insertUpdateQuote mutation

        This method automatically creates quote items from the request's items.
        For each request item with provider_items assigned, a corresponding quote item is created.

        Note:
        - Default status: 'initial' - Quote has been created but not yet being worked on
        - 'rounds' (negotiation rounds) is auto-calculated by backend based on existing quotes from the same provider
        - shipping_method and shipping_amount cannot be set during creation, use update_quote instead
        - Quote items are automatically created from request items with provider_items
        - After creation, quote items can be managed using update_quote_item
        - Request must be in 'confirmed' status to create quotes
        """
        self.logger.info(f"Creating quote: {arguments}")

        # Validate request status allows quote creation
        request = self.get_rfq_request(request_uuid=arguments["request_uuid"])
        if error := propagate_error_if_present(request):
            return error

        request_status = request.get("status", "")
        RequestOperationGuard.validate_can_create_quote(request_status)

        # First, create the quote
        variables = {
            "requestUuid": arguments["request_uuid"],
            "providerCorpExternalId": arguments["provider_corp_external_id"],
            "salesRepEmail": arguments.get("sales_rep_email"),
            "segmentUuid": arguments.get("segment_uuid"),
            "status": arguments.get("status", QuoteStatus.INITIAL),
            "notes": arguments.get("notes", ""),
            "updatedBy": "MCP",
        }

        # Remove None values to only send provided fields
        # Note: 'rounds' is auto-calculated, shipping_method/shipping_amount not allowed on creation
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "insertUpdateQuote",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        quote = humps.decamelize(result["quote"])

        # We already have the request from validation above
        # Create quote items from request items that have provider_items assigned
        request_items = request.get("items", [])
        provider_corp_external_id = arguments["provider_corp_external_id"]
        created_quote_item_count = 0
        quote_item_errors = []

        if request_items:
            self.logger.info(
                f"Creating quote items from {len(request_items)} request items for provider {provider_corp_external_id}"
            )

            for req_item in request_items:
                provider_items = req_item.get("provider_items", [])

                if provider_items:
                    # Filter provider_items to only include those matching the quote's provider
                    matching_provider_items = [
                        pi
                        for pi in provider_items
                        if pi.get("provider_corp_external_id")
                        == provider_corp_external_id
                    ]

                    if not matching_provider_items:
                        self.logger.info(
                            f"Skipping request item {req_item.get('item_uuid')} - no provider_items for provider {provider_corp_external_id}"
                        )
                        continue

                    # Create a quote item for each matching provider_item
                    for provider_item in matching_provider_items:
                        quote_item_args = {
                            "quote_uuid": quote["quote_uuid"],
                            "provider_item_uuid": provider_item.get(
                                "provider_item_uuid"
                            ),
                            "item_uuid": req_item.get("item_uuid"),
                            "qty": provider_item.get("qty", req_item.get("qty", 0)),
                            "pax_breakdown": req_item.get("pax_breakdown"),
                            "segment_uuid": arguments.get("segment_uuid") or "default",
                            "batch_no": provider_item.get("batch_no")
                            or arguments.get("batch_no"),
                            "service_start_at": provider_item.get("service_start_at")
                            or arguments.get("service_start_at"),
                            "service_end_at": provider_item.get("service_end_at")
                            or arguments.get("service_end_at"),
                            "request_data": req_item.get("request_data"),
                            "request_uuid": arguments["request_uuid"],
                        }

                        # Use the private method to add quote item
                        quote_item_result = self._add_quote_item(**quote_item_args)

                        # Check if there was an error creating the quote item
                        if error := propagate_error_if_present(quote_item_result):
                            self.logger.error(
                                f"Failed to create quote item for provider_item {provider_item.get('provider_item_uuid')}: {error}"
                            )
                            quote_item_errors.append(error)
                            # Continue creating other quote items even if one fails
                            continue

                        self.logger.info(
                            f"Created quote item for provider_item {provider_item.get('provider_item_uuid')}"
                        )
                        created_quote_item_count += 1
                else:
                    self.logger.info(
                        f"Skipping request item {req_item.get('item_uuid')} - no provider_items assigned"
                    )

        if quote_item_errors and created_quote_item_count == 0:
            return build_error_response(
                "Quote was created but no quote items could be created",
                ErrorCode.OPERATION_FAILED,
                {
                    "quote_uuid": quote.get("quote_uuid"),
                    "quote_item_errors": quote_item_errors,
                },
            )

        # Return the quote (quote items were already created)
        # Note: The quote object may not include the newly created quote_items
        # If you need the full quote with items, call get_quote separately
        return quote

    # * Private helper method (not exposed as MCP tool)
    @handle_errors(operation_name="add quote item")
    def _add_quote_item(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a quote item to an existing quote.
        This is a convenience method that adds a new item using insertUpdateQuoteItem mutation.

        Args:
            quote_uuid: UUID of the quote
            provider_item_uuid: UUID of the provider item
            item_uuid: UUID of the item
            qty: Quantity
            segment_uuid: UUID of the segment (optional)
            batch_no: Batch number (optional, enables slow_move_item tracking)
            request_data: Request data (optional)
            discount_amount: Discount amount (optional)

        Returns:
            Created quote item with:
            - slow_move_item: Boolean flag (true if batch has slow-moving inventory)
            - guardrail_price_per_uom: Minimum acceptable price
        """
        self.logger.info(f"Adding quote item: {arguments}")

        # Get current quote to check status
        get_quote_args = {"quote_uuid": arguments["quote_uuid"]}
        if "request_uuid" in arguments:
            get_quote_args["request_uuid"] = arguments["request_uuid"]

        current_quote = self.get_quote(**get_quote_args)
        if error := propagate_error_if_present(current_quote):
            return error

        # Validate that quote status allows item modifications
        current_status = current_quote.get("status", "")
        QuoteOperationGuard.validate_can_modify_items(current_status)

        # Check if quote status should be auto-updated to in_progress
        should_update_status = False
        if current_status == QuoteStatus.INITIAL:
            should_update_status = True
            self.logger.info(
                f"Quote status will be changed to 'in_progress' because items are being actively added"
            )

        variables = {
            "quoteUuid": arguments["quote_uuid"],
            "providerItemUuid": arguments.get("provider_item_uuid"),
            "itemUuid": arguments.get("item_uuid"),
            "qty": float(arguments["qty"]) if arguments.get("qty") is not None else None,
            "segmentUuid": arguments.get("segment_uuid") or "default",
            "batchNo": arguments.get("batch_no"),
            "serviceStartAt": arguments.get("service_start_at"),
            "serviceEndAt": arguments.get("service_end_at"),
            "paxBreakdown": arguments.get("pax_breakdown"),
            "requestUuid": arguments.get("request_uuid"),
            "requestData": arguments.get("request_data"),
            "subtotalDiscount": float(arguments.get("discount_amount", 0.0)),
            "updatedBy": "MCP",
        }

        # Remove None values (but keep "default" for segment_uuid)
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "insertUpdateQuoteItem",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        quote_item = humps.decamelize(result["quoteItem"])

        self.logger.info(
            f"Successfully added quote item to quote {arguments['quote_uuid']}"
        )

        # Update quote status to in_progress if needed
        if should_update_status:
            update_args = {
                "quote_uuid": arguments["quote_uuid"],
                "status": QuoteStatus.IN_PROGRESS,
            }
            if "request_uuid" in arguments:
                update_args["request_uuid"] = arguments["request_uuid"]

            update_result = self.update_quote(**update_args)
            if error := propagate_error_if_present(update_result):
                self.logger.warning(
                    f"Failed to update quote status to in_progress: {error}"
                )

        return quote_item

    # ==================== Quote Management Tools ====================

    # * MCP Function.
    @handle_errors(operation_name="update quote")
    def update_quote(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update quote metadata (shipping, status, notes).
        Maps to GraphQL: insertUpdateQuote mutation

        Can update:
        - shipping_method, shipping_amount (only in 'initial' or 'in_progress' status)
        - status (validated according to status flow)
        - notes

        Note: 'rounds' (negotiation rounds) are auto-calculated by the backend based on existing quotes from the same provider.
        Cannot modify quote items - use update_quote_item instead.

        Status transitions are validated according to the quote status flow.
        Shipping/notes updates require quote to be in 'initial' or 'in_progress' status.
        """
        self.logger.info(f"Updating quote: {arguments}")

        # Get current quote to check current status
        current_quote = self.get_quote(
            request_uuid=arguments["request_uuid"],
            quote_uuid=arguments["quote_uuid"],
        )
        if error := propagate_error_if_present(current_quote):
            return error

        current_status = current_quote.get("status", "")

        # Validate status transition if status is being updated
        if "status" in arguments:
            new_status = arguments["status"]
            # Validate the transition
            QuoteStatusTransitions.validate_transition(current_status, new_status)

        # Validate that quote status allows metadata modifications (shipping, notes)
        # Only apply this validation if we're NOT doing a status change
        # (Status changes can include notes to document the reason for the change)
        is_updating_metadata = any(
            key in arguments for key in ["shipping_method", "shipping_amount", "notes"]
        )
        if is_updating_metadata and "status" not in arguments:
            QuoteOperationGuard.validate_can_modify_items(current_status)

        variables = {
            "requestUuid": arguments["request_uuid"],
            "quoteUuid": arguments["quote_uuid"],
            "shippingMethod": arguments.get("shipping_method"),
            "shippingAmount": arguments.get("shipping_amount"),
            "status": arguments.get("status"),
            "notes": arguments.get("notes"),
            "updatedBy": "MCP",
        }

        # Remove None values to only update provided fields
        # Note: 'rounds' is auto-calculated by backend, not sent in updates
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "insertUpdateQuote",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        quote = humps.decamelize(result["quote"])

        return quote

    # * MCP Function.
    @handle_errors(operation_name="get quote")
    def get_quote(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve quote details.
        Maps to GraphQL: quote query

        Response includes:
        - quote_items: Array of quote items with slow_move_item flags and guardrail pricing
        - rounds: Negotiation round number (auto-calculated based on provider's quote history for this request)
        """
        variables = {
            "quoteUuid": arguments["quote_uuid"],
        }

        # Add requestUuid if provided (may be required by GraphQL schema)
        if "request_uuid" in arguments:
            variables["requestUuid"] = arguments["request_uuid"]

        result = self._execute_graphql_query(
            "ai_rfq_graphql", "quote", "Query", variables
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        # Handle case where result might be a JSON string instead of a dict
        if isinstance(result, str):
            import json

            # Empty string means no data found - return empty dict
            if not result.strip():
                return {}
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                self.logger.error(
                    f"Failed to parse quote JSON string: {result[:200]}"
                )
                return {}

        # Check if result is None or empty - return empty dict
        if not result:
            return {}

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="search quotes")
    def search_quotes(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search quotes with filters.
        Maps to GraphQL: quoteList query
        """
        variables = {
            "pageNumber": arguments.get("page_number", 1),
            "limit": arguments.get("limit", 20),
            "requestUuid": arguments.get("request_uuid"),
            "providerCorpExternalId": arguments.get("provider_corp_external_id"),
            "statuses": arguments.get("statuses"),
            "fromCreatedAt": arguments.get("from_created_at"),
            "toCreatedAt": arguments.get("to_created_at"),
        }

        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "quoteList",
            "Query",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        return humps.decamelize(result)

    # * MCP Function.
    @handle_errors(operation_name="update quote item")
    def update_quote_item(self, **arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing quote item (discount amount only).
        Maps to GraphQL: insertUpdateQuoteItem mutation

        Note: Only discount_amount can be updated. Other fields (qty, provider_item_uuid, etc.)
        are read-only after creation. To modify other properties, remove and re-add the item.

        Requirements:
        - Quote must be in 'initial' or 'in_progress' status to modify items

        Response includes:
        - slow_move_item: Boolean flag indicating if item is from slow-moving inventory
        - guardrail_price_per_uom: Minimum acceptable price for profitability
        """
        self.logger.info(f"Updating quote item: {arguments}")

        # Get current quote to check status
        get_quote_args = {"quote_uuid": arguments["quote_uuid"]}
        if "request_uuid" in arguments:
            get_quote_args["request_uuid"] = arguments["request_uuid"]

        current_quote = self.get_quote(**get_quote_args)
        if error := propagate_error_if_present(current_quote):
            return error

        # Validate that quote status allows item modifications
        current_status = current_quote.get("status", "")
        QuoteOperationGuard.validate_can_modify_items(current_status)

        variables = {
            "quoteUuid": arguments["quote_uuid"],
            "quoteItemUuid": arguments.get("quote_item_uuid"),
            "requestUuid": arguments.get("request_uuid"),
            "subtotalDiscount": float(arguments.get("discount_amount", 0.0)),
            "notes": arguments.get("notes"),
            "updatedBy": "MCP",
        }

        # Remove None values
        variables = {k: v for k, v in variables.items() if v is not None and v != ""}

        result = self._execute_graphql_query(
            "ai_rfq_graphql",
            "insertUpdateQuoteItem",
            "Mutation",
            variables,
        )

        # Check for error in response and propagate if present
        if error := propagate_error_if_present(result):
            return error

        quote_item = humps.decamelize(result["quoteItem"])

        return quote_item

    # * MCP Function.
    @handle_errors(operation_name="confirm quote and create installments")
    def confirm_quote_and_create_installments(
        self, **arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Confirm a selected quote and create installment plan.

        This is a convenience method that:
        1. Updates the quote status to 'confirmed'
        2. Creates either a single installment for full amount or multiple installments
        3. Disapproves all other quotes for the same request
        4. Returns confirmed quote and created installments

        Args:
            request_uuid: UUID of the request
            quote_uuid: UUID of the quote to confirm
            create_single_installment: If True, creates one installment for full amount (default: True)
            interval_num: Number of installments (required if create_single_installment=False)
            total_pay_period: Total payment period in months (required if create_single_installment=False)
            payment_method: Optional payment method for installments

        Returns:
            Dictionary with confirmed quote and created installments
        """
        self.logger.info(f"Confirming quote and creating installments: {arguments}")

        request_uuid = arguments["request_uuid"]
        quote_uuid = arguments["quote_uuid"]
        create_single_installment = arguments.get("create_single_installment", True)
        payment_method = arguments.get("payment_method")

        # Validate inputs
        validate_not_empty(request_uuid, "request_uuid", "Request UUID is required")
        validate_not_empty(quote_uuid, "quote_uuid", "Quote UUID is required")

        if not create_single_installment:
            interval_num = arguments.get("interval_num")
            total_pay_period = arguments.get("total_pay_period")

            validate_not_empty(
                interval_num,
                "interval_num",
                "interval_num is required for multiple installments",
            )
            validate_not_empty(
                total_pay_period,
                "total_pay_period",
                "total_pay_period is required for multiple installments",
            )

            if interval_num <= 0:
                return build_error_response(
                    message="interval_num must be greater than 0",
                    error_code=ErrorCode.VALIDATION_FAILED,
                )

            if total_pay_period <= 0:
                return build_error_response(
                    message="total_pay_period must be greater than 0",
                    error_code=ErrorCode.VALIDATION_FAILED,
                )

        # Validate quote status allows confirmation
        current_quote = self.get_quote(request_uuid=request_uuid, quote_uuid=quote_uuid)
        if error := propagate_error_if_present(current_quote):
            return error

        current_status = current_quote.get("status", "")
        # Validate the transition to confirmed
        QuoteStatusTransitions.validate_transition(
            current_status, QuoteStatus.CONFIRMED
        )

        # Step 1: Update quote status to confirmed
        self.logger.info(f"Updating quote {quote_uuid} status to confirmed")

        confirmed_quote = self.update_quote(
            request_uuid=request_uuid,
            quote_uuid=quote_uuid,
            status=QuoteStatus.CONFIRMED,
        )

        if error := propagate_error_if_present(confirmed_quote):
            return error

        # Business Rule: Disapprove all other quotes for this request when one is confirmed
        self.logger.info(
            f"Quote {quote_uuid} confirmed, disapproving all other quotes for request {request_uuid}"
        )

        # Get all quotes for this request
        quotes_result = self.search_quotes(
            request_uuid=request_uuid,
            limit=100,
        )

        if not propagate_error_if_present(quotes_result):
            all_quotes = quotes_result.get("quote_list", [])

            # Filter quotes that should be disapproved
            # Exclude: the confirmed quote, already in terminal states (disapproved, completed)
            terminal_statuses = [
                QuoteStatus.DISAPPROVED,
                QuoteStatus.COMPLETED,
            ]
            quotes_to_disapprove = [
                q
                for q in all_quotes
                if q.get("quote_uuid") != quote_uuid
                and q.get("status") not in terminal_statuses
            ]

            # Disapprove each quote
            for quote_to_disapprove in quotes_to_disapprove:
                disapprove_quote_uuid = quote_to_disapprove.get("quote_uuid")
                self.logger.info(f"Disapproving quote {disapprove_quote_uuid}")

                disapprove_result = self.update_quote(
                    request_uuid=request_uuid,
                    quote_uuid=disapprove_quote_uuid,
                    status=QuoteStatus.DISAPPROVED,
                    notes="Auto-disapproved: Another quote was confirmed",
                )

                if error := propagate_error_if_present(disapprove_result):
                    self.logger.error(
                        f"Failed to disapprove quote {disapprove_quote_uuid}: {error}"
                    )
                else:
                    self.logger.info(
                        f"Successfully disapproved quote {disapprove_quote_uuid}"
                    )

        # Step 2: Create installments
        installments_result = None

        if create_single_installment:
            # Create single installment for full amount
            self.logger.info(f"Creating single installment for full quote amount")

            installment_args = {
                "request_uuid": request_uuid,
                "quote_uuid": quote_uuid,
                "status": "pending",
            }

            if payment_method:
                installment_args["payment_method"] = payment_method

            installments_result = self._create_installment(**installment_args)

            if error := propagate_error_if_present(installments_result):
                error_msg = error.get("error", "Unknown error") if isinstance(error, dict) else str(error)
                return build_error_response(
                    message=f"Quote confirmed but failed to create installment: {error_msg}",
                    error_code=ErrorCode.OPERATION_FAILED,
                    details={
                        "confirmed_quote": confirmed_quote,
                        "installment_error": error,
                    },
                )

            # Wrap single installment in array for consistent response format
            installments_result = {
                "installments": [installments_result],
                "total_created": 1,
                "installment_amount_per": installments_result.get("installment_amount"),
                "total_installment_amount": installments_result.get(
                    "installment_amount"
                ),
            }

        else:
            # Create multiple installments
            self.logger.info(
                f"Creating {arguments['interval_num']} installments over {arguments['total_pay_period']} months"
            )

            installments_args = {
                "request_uuid": request_uuid,
                "quote_uuid": quote_uuid,
                "interval_num": arguments["interval_num"],
                "total_pay_period": arguments["total_pay_period"],
            }

            if payment_method:
                installments_args["payment_method"] = payment_method

            installments_result = self._create_installments(**installments_args)

            if error := propagate_error_if_present(installments_result):
                error_msg = error.get("error", "Unknown error") if isinstance(error, dict) else str(error)
                return build_error_response(
                    message=f"Quote confirmed but failed to create installments: {error_msg}",
                    error_code=ErrorCode.OPERATION_FAILED,
                    details={
                        "confirmed_quote": confirmed_quote,
                        "installments_error": error,
                    },
                )

        # Get updated quote with full details
        final_quote = self.get_quote(request_uuid=request_uuid, quote_uuid=quote_uuid)

        if error := propagate_error_if_present(final_quote):
            # Use confirmed_quote if we can't get updated details
            final_quote = confirmed_quote

        # Return summary
        result = {
            "quote": final_quote,
            "installments": installments_result.get("installments", []),
            "total_installments_created": installments_result.get("total_created", 0),
            "installment_amount_per": installments_result.get("installment_amount_per"),
            "total_installment_amount": installments_result.get(
                "total_installment_amount"
            ),
            "installment_type": "single" if create_single_installment else "multiple",
        }

        self.logger.info(
            f"Quote confirmation completed: Quote {quote_uuid} confirmed with {result['total_installments_created']} installment(s) created"
        )

        return result
