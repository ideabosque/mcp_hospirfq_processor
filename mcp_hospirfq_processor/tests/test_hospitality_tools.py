#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for the 11 new hospitality MCP tools.

All tests mock _execute_graphql_query so no external services are required.
Tests cover:
  - AvailabilityMixin: check_availability, acquire_availability_hold,
    release_availability_hold, confirm_availability_hold, expire_availability_hold
  - BundleMixin: search_bundles, get_bundle, search_bundle_components
  - CancellationMixin: get_cancellation_policy, search_cancellation_policies
  - CatalogMixin: inquire_catalog

Also covers:
  - StatusManager: AvailabilityHoldStatus transitions
  - ErrorHandler: hospitality-specific error codes
  - Facade MRO: all 38 tool methods resolve
"""

from __future__ import annotations

__author__ = "Idea Bosque"

import logging

import pytest

logger = logging.getLogger("test_mcp_hospirfq_processor")


# ============================================================================
# AvailabilityMixin — 5 tools
# ============================================================================


class TestCheckAvailability:
    """check_availability: query available capacity for a service window."""

    @pytest.mark.unit
    def test_returns_availability_data(self, processor):
        processor._execute_graphql_query.return_value = {
            "availableQty": 10,
            "serviceStartAt": "2026-08-15T14:00:00Z",
            "serviceEndAt": "2026-08-15T18:00:00Z",
        }
        result = processor.check_availability(
            partition_key="HOTEL-001",
            provider_item_uuid="pi-789",
            service_start_at="2026-08-15T14:00:00Z",
            service_end_at="2026-08-15T18:00:00Z",
        )
        assert "error" not in result
        assert result["available_qty"] == 10

    @pytest.mark.unit
    def test_passes_camelcase_variables(self, processor):
        processor._execute_graphql_query.return_value = {"availableQty": 5}
        processor.check_availability(
            partition_key="HOTEL-001",
            provider_item_uuid="pi-789",
            service_start_at="2026-08-15",
            service_end_at="2026-08-18",
            batch_no="STD",
            qty=2,
        )
        call_args = processor._execute_graphql_query.call_args
        variables = call_args[1].get("variables", call_args[0][3])
        # camelCase keys
        assert "partitionKey" in variables
        assert "providerItemUuid" in variables
        assert "serviceStartAt" in variables
        assert "serviceEndAt" in variables
        assert "batchNo" in variables
        # values
        assert variables["partitionKey"] == "HOTEL-001"
        assert variables["providerItemUuid"] == "pi-789"

    @pytest.mark.unit
    def test_optional_fields_omitted_when_none(self, processor):
        processor._execute_graphql_query.return_value = {"availableQty": 3}
        processor.check_availability(
            partition_key="PK",
            provider_item_uuid="pi-1",
            service_start_at="2026-01-01",
            service_end_at="2026-01-02",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "batchNo" not in variables
        assert "qty" not in variables


class TestAcquireAvailabilityHold:
    """acquire_availability_hold: atomically reserve capacity."""

    @pytest.mark.unit
    def test_successful_hold(self, processor):
        processor._execute_graphql_query.return_value = {
            "holdToken": "hold-abc123",
            "status": "held",
            "expiresAt": "2026-08-15T15:30:00Z",
        }
        result = processor.acquire_availability_hold(
            partition_key="HOTEL-001",
            provider_item_uuid="pi-789",
            service_start_at="2026-08-15T14:00:00Z",
            service_end_at="2026-08-18T11:00:00Z",
            qty=2,
        )
        assert "error" not in result
        assert result["hold_token"] == "hold-abc123"
        assert result["status"] == "held"

    @pytest.mark.unit
    def test_mutation_includes_updated_by(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-1", "status": "held"}
        processor.acquire_availability_hold(
            partition_key="PK",
            provider_item_uuid="pi-1",
            service_start_at="2026-01-01",
            service_end_at="2026-01-03",
            qty=1,
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["updatedBy"] == "MCP"

    @pytest.mark.unit
    def test_pax_breakdown_included(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-2", "status": "held"}
        pax = {"adult": 2, "child": 1, "infant": 0}
        processor.acquire_availability_hold(
            partition_key="PK",
            provider_item_uuid="pi-1",
            service_start_at="2026-01-01",
            service_end_at="2026-01-03",
            qty=3,
            pax_breakdown=pax,
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "paxBreakdown" in variables
        assert variables["paxBreakdown"]["adult"] == 2

    @pytest.mark.unit
    def test_quote_link_optional(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-3", "status": "held"}
        processor.acquire_availability_hold(
            partition_key="PK",
            provider_item_uuid="pi-1",
            service_start_at="2026-01-01",
            service_end_at="2026-01-03",
            qty=1,
            quote_uuid="q-100",
            quote_item_uuid="qi-200",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["quoteUuid"] == "q-100"
        assert variables["quoteItemUuid"] == "qi-200"


class TestReleaseAvailabilityHold:
    """release_availability_hold: release held capacity (idempotent)."""

    @pytest.mark.unit
    def test_successful_release(self, processor):
        processor._execute_graphql_query.return_value = {
            "holdToken": "hold-abc123",
            "status": "released",
        }
        result = processor.release_availability_hold(
            partition_key="HOTEL-001",
            hold_token="hold-abc123",
            provider_item_uuid="pi-789",
        )
        assert "error" not in result
        assert result["status"] == "released"

    @pytest.mark.unit
    def test_mutation_includes_updated_by(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-1", "status": "released"}
        processor.release_availability_hold(
            partition_key="PK",
            hold_token="ht-1",
            provider_item_uuid="pi-1",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["updatedBy"] == "MCP"
        assert variables["holdToken"] == "ht-1"
        assert variables["partitionKey"] == "PK"
        assert variables["providerItemUuid"] == "pi-1"


class TestConfirmAvailabilityHold:
    """confirm_availability_hold: confirm held reservation (no 2nd decrement)."""

    @pytest.mark.unit
    def test_successful_confirm(self, processor):
        processor._execute_graphql_query.return_value = {
            "holdToken": "hold-abc123",
            "status": "confirmed",
        }
        result = processor.confirm_availability_hold(
            partition_key="HOTEL-001",
            hold_token="hold-abc123",
            provider_item_uuid="pi-789",
        )
        assert "error" not in result
        assert result["status"] == "confirmed"

    @pytest.mark.unit
    def test_mutation_includes_updated_by(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-1", "status": "confirmed"}
        processor.confirm_availability_hold(
            partition_key="PK",
            hold_token="ht-1",
            provider_item_uuid="pi-1",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["updatedBy"] == "MCP"
        assert variables["providerItemUuid"] == "pi-1"


class TestExpireAvailabilityHold:
    """expire_availability_hold: expire stale hold and restore capacity."""

    @pytest.mark.unit
    def test_successful_expire(self, processor):
        processor._execute_graphql_query.return_value = {
            "holdToken": "hold-abc123",
            "status": "expired",
        }
        result = processor.expire_availability_hold(
            partition_key="HOTEL-001",
            hold_token="hold-abc123",
            provider_item_uuid="pi-789",
        )
        assert "error" not in result
        assert result["status"] == "expired"

    @pytest.mark.unit
    def test_mutation_includes_updated_by(self, processor):
        processor._execute_graphql_query.return_value = {"holdToken": "ht-1", "status": "expired"}
        processor.expire_availability_hold(
            partition_key="PK",
            hold_token="ht-1",
            provider_item_uuid="pi-1",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["updatedBy"] == "MCP"
        assert variables["providerItemUuid"] == "pi-1"


# ============================================================================
# BundleMixin — 3 tools
# ============================================================================


class TestSearchBundles:
    """search_bundles: list package and itinerary templates."""

    @pytest.mark.unit
    def test_returns_bundle_list(self, processor):
        processor._execute_graphql_query.return_value = [
            {"bundleUuid": "b-1", "bundleCode": "PKG-SEA", "bundleType": "package"},
            {"bundleUuid": "b-2", "bundleCode": "FLT-NYC-LAX", "bundleType": "itinerary"},
        ]
        result = processor.search_bundles(
            partition_key="HOTEL-001",
        )
        assert "error" not in result
        assert len(result) == 2
        assert result[0]["bundle_code"] == "PKG-SEA"

    @pytest.mark.unit
    def test_filters_by_type(self, processor):
        processor._execute_graphql_query.return_value = [
            {"bundleUuid": "b-2", "bundleType": "itinerary"},
        ]
        processor.search_bundles(
            partition_key="PK",
            bundle_type="itinerary",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["bundleType"] == "itinerary"

    @pytest.mark.unit
    def test_optional_params_omitted(self, processor):
        processor._execute_graphql_query.return_value = []
        processor.search_bundles(partition_key="PK")
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "bundleCode" not in variables
        assert "bundleType" not in variables
        assert "status" not in variables


class TestGetBundle:
    """get_bundle: fetch a single bundle with nested components."""

    @pytest.mark.unit
    def test_returns_bundle_detail(self, processor):
        processor._execute_graphql_query.return_value = {
            "bundleUuid": "b-1",
            "bundleCode": "PKG-SEA",
            "bundleType": "package",
            "components": [
                {"componentUuid": "c-1", "itemType": "hotel_room"},
            ],
        }
        result = processor.get_bundle(
            partition_key="HOTEL-001",
            bundle_uuid="b-1",
        )
        assert "error" not in result
        assert result["bundle_uuid"] == "b-1"
        assert len(result["components"]) == 1

    @pytest.mark.unit
    def test_camelcase_variables(self, processor):
        processor._execute_graphql_query.return_value = {"bundleUuid": "b-1"}
        processor.get_bundle(partition_key="PK", bundle_uuid="b-1")
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "bundleUuid" in variables
        assert "partitionKey" in variables


class TestSearchBundleComponents:
    """search_bundle_components: list components for a bundle."""

    @pytest.mark.unit
    def test_returns_component_list(self, processor):
        processor._execute_graphql_query.return_value = [
            {"componentUuid": "c-1", "itemType": "hotel_room", "qty": 2},
            {"componentUuid": "c-2", "itemType": "flight", "qty": 1},
        ]
        result = processor.search_bundle_components(
            partition_key="HOTEL-001",
            bundle_uuid="b-1",
        )
        assert "error" not in result
        assert len(result) == 2
        assert result[1]["item_type"] == "flight"


# ============================================================================
# CancellationMixin — 2 tools
# ============================================================================


class TestGetCancellationPolicy:
    """get_cancellation_policy: fetch a policy by UUID."""

    @pytest.mark.unit
    def test_returns_policy(self, processor):
        processor._execute_graphql_query.return_value = {
            "policyUuid": "pol-1",
            "providerItemUuid": "pi-789",
            "tiers": [
                {"hoursBeforeServiceGte": 72, "refundPercentage": 100},
                {"hoursBeforeServiceGte": 24, "refundPercentage": 50},
                {"hoursBeforeServiceGte": 0, "refundPercentage": 0},
            ],
        }
        result = processor.get_cancellation_policy(
            partition_key="HOTEL-001",
            policy_uuid="pol-1",
        )
        assert "error" not in result
        assert result["policy_uuid"] == "pol-1"
        assert len(result["tiers"]) == 3
        assert result["tiers"][0]["refund_percentage"] == 100

    @pytest.mark.unit
    def test_camelcase_variables(self, processor):
        processor._execute_graphql_query.return_value = {"policyUuid": "pol-1"}
        processor.get_cancellation_policy(partition_key="PK", policy_uuid="pol-1")
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "policyUuid" in variables
        assert "partitionKey" in variables


class TestSearchCancellationPolicies:
    """search_cancellation_policies: list policies for a provider item."""

    @pytest.mark.unit
    def test_returns_policy_list(self, processor):
        processor._execute_graphql_query.return_value = [
            {"policyUuid": "pol-1", "status": "active"},
            {"policyUuid": "pol-2", "status": "active"},
        ]
        result = processor.search_cancellation_policies(
            partition_key="HOTEL-001",
            provider_item_uuid="pi-789",
        )
        assert "error" not in result
        assert len(result) == 2

    @pytest.mark.unit
    def test_optional_status_filter(self, processor):
        processor._execute_graphql_query.return_value = []
        processor.search_cancellation_policies(
            partition_key="PK",
            status="active",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["status"] == "active"
        assert "providerItemUuid" not in variables


# ============================================================================
# CatalogMixin — 1 tool
# ============================================================================


class TestInquireCatalog:
    """inquire_catalog: search Knowledge Graph Engine for products."""

    @pytest.mark.unit
    def test_returns_catalog_results(self, processor):
        processor._execute_graphql_query.return_value = [
            {"itemUuid": "i-1", "itemName": "Deluxe Ocean View", "score": 0.95},
            {"itemUuid": "i-2", "itemName": "Standard Room", "score": 0.72},
        ]
        result = processor.inquire_catalog(
            partition_key="HOTEL-001",
            query_text="ocean view room",
        )
        assert "error" not in result
        assert len(result) == 2
        assert result[0]["item_name"] == "Deluxe Ocean View"

    @pytest.mark.unit
    def test_optional_namespace_and_limit(self, processor):
        processor._execute_graphql_query.return_value = []
        processor.inquire_catalog(
            partition_key="PK",
            query_text="flight to paris",
            namespace="flights",
            limit=5,
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["namespace"] == "flights"
        assert variables["query"]["limit"] == 5
        assert variables["query"]["topK"] == 5

    @pytest.mark.unit
    def test_required_fields_only(self, processor):
        processor._execute_graphql_query.return_value = []
        processor.inquire_catalog(
            partition_key="PK",
            query_text="hotel",
        )
        variables = processor._execute_graphql_query.call_args[0][3]
        assert "namespace" not in variables
        assert variables["query"]["queryText"] == "hotel"


# ============================================================================
# StatusManager — AvailabilityHoldStatus transitions
# ============================================================================


class TestAvailabilityHoldStatusTransitions:
    """Verify hold status transition rules."""

    @pytest.mark.unit
    def test_held_to_confirmed(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert AvailabilityHoldStatusTransitions.is_valid_transition("held", "confirmed")

    @pytest.mark.unit
    def test_held_to_released(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert AvailabilityHoldStatusTransitions.is_valid_transition("held", "released")

    @pytest.mark.unit
    def test_held_to_expired(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert AvailabilityHoldStatusTransitions.is_valid_transition("held", "expired")

    @pytest.mark.unit
    def test_confirmed_is_terminal(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert not AvailabilityHoldStatusTransitions.is_valid_transition("confirmed", "released")
        assert not AvailabilityHoldStatusTransitions.is_valid_transition("confirmed", "expired")

    @pytest.mark.unit
    def test_released_is_terminal(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert not AvailabilityHoldStatusTransitions.is_valid_transition("released", "held")

    @pytest.mark.unit
    def test_expired_is_terminal(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        assert not AvailabilityHoldStatusTransitions.is_valid_transition("expired", "held")

    @pytest.mark.unit
    def test_same_status_is_valid(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        for status in ("held", "confirmed", "released", "expired"):
            assert AvailabilityHoldStatusTransitions.is_valid_transition(status, status)

    @pytest.mark.unit
    def test_invalid_transition_raises(self):
        from mcp_hospirfq_processor.status_manager import (
            AvailabilityHoldStatusTransitions,
        )
        from mcp_hospirfq_processor.error_handler import ValidationError
        with pytest.raises(ValidationError):
            AvailabilityHoldStatusTransitions.validate_transition("confirmed", "released")


# ============================================================================
# ErrorHandler — hospitality-specific error codes
# ============================================================================


class TestHospitalityErrorCodes:
    """Verify hospitality error codes exist and build correct responses."""

    @pytest.mark.unit
    def test_hold_not_found_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.HOLD_NOT_FOUND == "HOLD_NOT_FOUND"

    @pytest.mark.unit
    def test_hold_already_confirmed_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.HOLD_ALREADY_CONFIRMED == "HOLD_ALREADY_CONFIRMED"

    @pytest.mark.unit
    def test_hold_already_released_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.HOLD_ALREADY_RELEASED == "HOLD_ALREADY_RELEASED"

    @pytest.mark.unit
    def test_hold_already_expired_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.HOLD_ALREADY_EXPIRED == "HOLD_ALREADY_EXPIRED"

    @pytest.mark.unit
    def test_availability_insufficient_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.AVAILABILITY_INSUFFICIENT == "AVAILABILITY_INSUFFICIENT"

    @pytest.mark.unit
    def test_bundle_not_found_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.BUNDLE_NOT_FOUND == "BUNDLE_NOT_FOUND"

    @pytest.mark.unit
    def test_cancel_policy_not_found_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.CANCEL_POLICY_NOT_FOUND == "CANCEL_POLICY_NOT_FOUND"

    @pytest.mark.unit
    def test_catalog_search_failed_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.CATALOG_SEARCH_FAILED == "CATALOG_SEARCH_FAILED"

    @pytest.mark.unit
    def test_pricing_mode_unsupported_code(self):
        from mcp_hospirfq_processor.error_handler import ErrorCode
        assert ErrorCode.PRICING_MODE_UNSUPPORTED == "PRICING_MODE_UNSUPPORTED"

    @pytest.mark.unit
    def test_build_error_response_with_hospitality_code(self):
        from mcp_hospirfq_processor.error_handler import (
            ErrorCode, build_error_response,
        )
        resp = build_error_response(
            "Only 3 rooms available",
            ErrorCode.AVAILABILITY_INSUFFICIENT,
            {"requested": 5, "available": 3},
        )
        assert resp["error"] == "Only 3 rooms available"
        assert resp["error_code"] == "AVAILABILITY_INSUFFICIENT"
        assert resp["details"]["requested"] == 5


# ============================================================================
# Facade MRO — all 38 tool methods resolve
# ============================================================================


class TestFacadeMRO:
    """Verify the flat mixin composition MRO and tool method resolution."""

    @pytest.mark.unit
    def test_mro_includes_all_mixins(self):
        from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor
        mro_names = [c.__name__ for c in MCPHospiRFQProcessor.__mro__]
        expected = [
            "MCPHospiRFQProcessor",
            "RequestMixin", "ItemMixin", "AvailabilityMixin",
            "QuoteMixin", "PricingMixin", "InstallmentMixin",
            "BundleMixin", "CancellationMixin", "FileMixin",
            "SegmentMixin", "CatalogMixin",
            "GraphQLBackedProcessor",
            "object",
        ]
        assert mro_names == expected

    @pytest.mark.unit
    def test_all_38_tool_methods_resolve(self):
        from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor
        # 27 existing tools (public names)
        existing_tools = [
            "submit_rfq_request", "update_rfq_request", "get_rfq_request",
            "search_rfq_requests", "add_item_to_rfq_request",
            "remove_item_from_rfq_request", "assign_provider_item_to_request_item",
            "remove_provider_item_from_request_item",
            "search_items", "get_item", "get_provider_items",
            "update_quote", "get_quote", "search_quotes", "update_quote_item",
            "get_item_price_tiers", "get_discount_prompts", "calculate_quote_pricing",
            "update_installment", "get_installments",
            "confirm_request_and_create_quotes",
            "confirm_quote_and_create_installments",
            "upload_rfq_file", "get_rfq_files", "get_segment_contacts",
        ]
        # 11 new hospitality tools
        new_tools = [
            "check_availability", "acquire_availability_hold",
            "release_availability_hold", "confirm_availability_hold",
            "expire_availability_hold",
            "search_bundles", "get_bundle", "search_bundle_components",
            "get_cancellation_policy", "search_cancellation_policies",
            "inquire_catalog",
        ]
        # 2 existing tools exposed via private methods (module_links mapping)
        private_tools = ["_create_installment", "_create_installments"]

        all_tools = existing_tools + new_tools + private_tools
        assert len(all_tools) == 38, f"Expected 38, got {len(all_tools)}"

        missing = [t for t in all_tools if not hasattr(MCPHospiRFQProcessor, t)]
        assert not missing, f"Missing tool methods: {missing}"

    @pytest.mark.unit
    def test_graphql_backed_processor_in_mro(self):
        from mcp_hospirfq_processor.mcp_hospirfq_processor import MCPHospiRFQProcessor
        assert hasattr(MCPHospiRFQProcessor, "_execute_graphql_query")


# ============================================================================
# Error propagation — GraphQL errors return clean error responses
# ============================================================================


class TestErrorPropagation:
    """Verify that GraphQL errors are properly caught and returned."""

    @pytest.mark.unit
    def test_graphql_error_returns_error_dict(self, processor):
        processor._execute_graphql_query.return_value = {
            "error": "GraphQL query failed",
            "error_code": "GRAPHQL_QUERY_FAILED",
        }
        result = processor.check_availability(
            partition_key="PK",
            provider_item_uuid="pi-1",
            service_start_at="2026-01-01",
            service_end_at="2026-01-02",
        )
        assert "error" in result
        assert result["error"] == "GraphQL query failed"

    @pytest.mark.unit
    def test_bundle_graphql_error_propagates(self, processor):
        processor._execute_graphql_query.return_value = {
            "error": "Bundle not found",
            "error_code": "BUNDLE_NOT_FOUND",
        }
        result = processor.get_bundle(partition_key="PK", bundle_uuid="b-999")
        assert "error" in result

    @pytest.mark.unit
    def test_cancellation_graphql_error_propagates(self, processor):
        processor._execute_graphql_query.return_value = {
            "error": "Policy not found",
            "error_code": "CANCEL_POLICY_NOT_FOUND",
        }
        result = processor.get_cancellation_policy(
            partition_key="PK", policy_uuid="pol-999",
        )
        assert "error" in result

    @pytest.mark.unit
    def test_catalog_graphql_error_propagates(self, processor):
        processor._execute_graphql_query.return_value = {
            "error": "KGE unavailable",
            "error_code": "CATALOG_SEARCH_FAILED",
        }
        result = processor.inquire_catalog(
            partition_key="PK", query_text="test",
        )
        assert "error" in result
