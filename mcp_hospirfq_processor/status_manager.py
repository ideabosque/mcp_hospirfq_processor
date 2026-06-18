#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Status management module for MCP HospiRFQ Processor.

Extends the base mcp_rfq_processor status manager with
AvailabilityHoldStatus for hospitality capacity reservations.
"""

from __future__ import annotations

__author__ = "Idea Bosque"

from typing import Dict, List, Optional, Set

from .error_handler import ErrorCode, ValidationError


# ==================== Status Constants ====================


class RequestStatus:
    """Valid statuses for RFQ Requests."""

    INITIAL = "initial"
    IN_PROGRESS = "in_progress"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    MODIFIED = "modified"

    @classmethod
    def all_values(cls) -> Set[str]:
        return {cls.INITIAL, cls.IN_PROGRESS, cls.CONFIRMED, cls.COMPLETED, cls.MODIFIED}

    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in cls.all_values()


class QuoteStatus:
    """Valid statuses for Quotes."""

    INITIAL = "initial"
    IN_PROGRESS = "in_progress"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    DISAPPROVED = "disapproved"

    @classmethod
    def all_values(cls) -> Set[str]:
        return {cls.INITIAL, cls.IN_PROGRESS, cls.CONFIRMED, cls.COMPLETED, cls.DISAPPROVED}

    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in cls.all_values()


class InstallmentStatus:
    """Valid statuses for Installments."""

    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"

    @classmethod
    def all_values(cls) -> Set[str]:
        return {cls.PENDING, cls.PAID, cls.CANCELLED}

    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in cls.all_values()


class AvailabilityHoldStatus:
    """Valid statuses for Availability Holds (hospitality-specific)."""

    HELD = "held"
    CONFIRMED = "confirmed"
    RELEASED = "released"
    EXPIRED = "expired"

    @classmethod
    def all_values(cls) -> Set[str]:
        return {cls.HELD, cls.CONFIRMED, cls.RELEASED, cls.EXPIRED}

    @classmethod
    def is_valid(cls, status: str) -> bool:
        return status in cls.all_values()


# ==================== Status Transition Rules ====================


class RequestStatusTransitions:
    """Valid status transitions for Requests."""

    ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
        RequestStatus.INITIAL: {RequestStatus.IN_PROGRESS, RequestStatus.CONFIRMED},
        RequestStatus.IN_PROGRESS: {RequestStatus.CONFIRMED, RequestStatus.MODIFIED},
        RequestStatus.CONFIRMED: {RequestStatus.COMPLETED, RequestStatus.MODIFIED},
        RequestStatus.MODIFIED: {RequestStatus.IN_PROGRESS, RequestStatus.CONFIRMED},
        RequestStatus.COMPLETED: set(),
    }

    @classmethod
    def is_valid_transition(cls, from_status: str, to_status: str) -> bool:
        if from_status == to_status:
            return True
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def validate_transition(cls, from_status: str, to_status: str) -> None:
        if not cls.is_valid_transition(from_status, to_status):
            allowed = cls.ALLOWED_TRANSITIONS.get(from_status, set())
            raise ValidationError(
                message=f"Invalid request status transition: '{from_status}' -> '{to_status}'. "
                f"Allowed transitions from '{from_status}': {sorted(allowed)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "from_status": from_status,
                    "to_status": to_status,
                    "allowed_transitions": sorted(allowed),
                },
            )


class QuoteStatusTransitions:
    """Valid status transitions for Quotes."""

    ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
        QuoteStatus.INITIAL: {QuoteStatus.IN_PROGRESS, QuoteStatus.CONFIRMED, QuoteStatus.DISAPPROVED},
        QuoteStatus.IN_PROGRESS: {QuoteStatus.CONFIRMED, QuoteStatus.DISAPPROVED},
        QuoteStatus.CONFIRMED: {QuoteStatus.COMPLETED, QuoteStatus.DISAPPROVED},
        QuoteStatus.COMPLETED: set(),
        QuoteStatus.DISAPPROVED: set(),
    }

    @classmethod
    def is_valid_transition(cls, from_status: str, to_status: str) -> bool:
        if from_status == to_status:
            return True
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def validate_transition(cls, from_status: str, to_status: str) -> None:
        if not cls.is_valid_transition(from_status, to_status):
            allowed = cls.ALLOWED_TRANSITIONS.get(from_status, set())
            raise ValidationError(
                message=f"Invalid quote status transition: '{from_status}' -> '{to_status}'. "
                f"Allowed transitions from '{from_status}': {sorted(allowed)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "from_status": from_status,
                    "to_status": to_status,
                    "allowed_transitions": sorted(allowed),
                },
            )


class InstallmentStatusTransitions:
    """Valid status transitions for Installments."""

    ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
        InstallmentStatus.PENDING: {InstallmentStatus.PAID, InstallmentStatus.CANCELLED},
        InstallmentStatus.PAID: set(),
        InstallmentStatus.CANCELLED: set(),
    }

    @classmethod
    def is_valid_transition(cls, from_status: str, to_status: str) -> bool:
        if from_status == to_status:
            return True
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def validate_transition(cls, from_status: str, to_status: str) -> None:
        if not cls.is_valid_transition(from_status, to_status):
            allowed = cls.ALLOWED_TRANSITIONS.get(from_status, set())
            raise ValidationError(
                message=f"Invalid installment status transition: '{from_status}' -> '{to_status}'. "
                f"Allowed transitions from '{from_status}': {sorted(allowed)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "from_status": from_status,
                    "to_status": to_status,
                    "allowed_transitions": sorted(allowed),
                },
            )


class AvailabilityHoldStatusTransitions:
    """Valid status transitions for Availability Holds.

    Key rules:
    - **Held → Confirmed**: reservation confirmed, no second capacity decrement
    - **Held → Released**: capacity restored once, idempotent
    - **Held → Expired**: capacity restored once, idempotent
    - Confirmed / Released / Expired are terminal states
    """

    ALLOWED_TRANSITIONS: Dict[str, Set[str]] = {
        AvailabilityHoldStatus.HELD: {
            AvailabilityHoldStatus.CONFIRMED,
            AvailabilityHoldStatus.RELEASED,
            AvailabilityHoldStatus.EXPIRED,
        },
        AvailabilityHoldStatus.CONFIRMED: set(),
        AvailabilityHoldStatus.RELEASED: set(),
        AvailabilityHoldStatus.EXPIRED: set(),
    }

    @classmethod
    def is_valid_transition(cls, from_status: str, to_status: str) -> bool:
        if from_status == to_status:
            return True
        return to_status in cls.ALLOWED_TRANSITIONS.get(from_status, set())

    @classmethod
    def validate_transition(cls, from_status: str, to_status: str) -> None:
        if not cls.is_valid_transition(from_status, to_status):
            allowed = cls.ALLOWED_TRANSITIONS.get(from_status, set())
            raise ValidationError(
                message=f"Invalid availability hold status transition: '{from_status}' -> '{to_status}'. "
                f"Allowed transitions from '{from_status}': {sorted(allowed)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "from_status": from_status,
                    "to_status": to_status,
                    "allowed_transitions": sorted(allowed),
                },
            )


# ==================== Operation Guards ====================


class RequestOperationGuard:
    """Guards for request operations based on status."""

    ALLOW_ITEM_MODIFICATIONS = {
        RequestStatus.INITIAL,
        RequestStatus.IN_PROGRESS,
        RequestStatus.MODIFIED,
    }
    ALLOW_QUOTE_CREATION = {RequestStatus.CONFIRMED}

    @classmethod
    def can_modify_items(cls, status: str) -> bool:
        return status in cls.ALLOW_ITEM_MODIFICATIONS

    @classmethod
    def validate_can_modify_items(cls, status: str) -> None:
        if not cls.can_modify_items(status):
            raise ValidationError(
                message=f"Cannot modify items: Request status is '{status}'. "
                f"Item modifications are only allowed in statuses: {sorted(cls.ALLOW_ITEM_MODIFICATIONS)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "current_status": status,
                    "allowed_statuses": sorted(cls.ALLOW_ITEM_MODIFICATIONS),
                },
            )

    @classmethod
    def can_create_quote(cls, status: str) -> bool:
        return status in cls.ALLOW_QUOTE_CREATION

    @classmethod
    def validate_can_create_quote(cls, status: str) -> None:
        if not cls.can_create_quote(status):
            raise ValidationError(
                message=f"Cannot create quote: Request status is '{status}'. "
                f"Quotes can only be created from requests with status: {sorted(cls.ALLOW_QUOTE_CREATION)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "current_status": status,
                    "allowed_statuses": sorted(cls.ALLOW_QUOTE_CREATION),
                },
            )


class QuoteOperationGuard:
    """Guards for quote operations based on status."""

    ALLOW_ITEM_MODIFICATIONS = {QuoteStatus.INITIAL, QuoteStatus.IN_PROGRESS}
    ALLOW_INSTALLMENT_CREATION = {QuoteStatus.CONFIRMED}

    @classmethod
    def can_modify_items(cls, status: str) -> bool:
        return status in cls.ALLOW_ITEM_MODIFICATIONS

    @classmethod
    def validate_can_modify_items(cls, status: str) -> None:
        if not cls.can_modify_items(status):
            raise ValidationError(
                message=f"Cannot modify quote items: Quote status is '{status}'. "
                f"Item modifications are only allowed in statuses: {sorted(cls.ALLOW_ITEM_MODIFICATIONS)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "current_status": status,
                    "allowed_statuses": sorted(cls.ALLOW_ITEM_MODIFICATIONS),
                },
            )

    @classmethod
    def can_create_installment(cls, status: str) -> bool:
        return status in cls.ALLOW_INSTALLMENT_CREATION

    @classmethod
    def validate_can_create_installment(cls, status: str) -> None:
        if not cls.can_create_installment(status):
            raise ValidationError(
                message=f"Cannot create installment: Quote status is '{status}'. "
                f"Installments can only be created for quotes with status: {sorted(cls.ALLOW_INSTALLMENT_CREATION)}",
                error_code=ErrorCode.VALIDATION_FAILED,
                details={
                    "current_status": status,
                    "allowed_statuses": sorted(cls.ALLOW_INSTALLMENT_CREATION),
                },
            )


# ==================== Automatic Status Update Logic ====================


def should_request_be_modified(
    current_status: str, items_changed: bool, has_quotes: bool
) -> bool:
    """When a confirmed request's items change and quotes exist → modified."""
    return current_status == RequestStatus.CONFIRMED and items_changed and has_quotes


def should_request_be_in_progress(current_status: str, items_changed: bool) -> bool:
    """When initial/modified request has items being actively worked on → in_progress."""
    return current_status in {RequestStatus.MODIFIED, RequestStatus.INITIAL} and items_changed


def should_quotes_be_disapproved(request_status: str) -> bool:
    """When request status changes to 'modified' → disapprove all quotes."""
    return request_status == RequestStatus.MODIFIED


def should_quote_be_completed(installments: List[Dict]) -> bool:
    """When all non-cancelled installments are paid → quote completed."""
    if not installments:
        return False
    active = [i for i in installments if i.get("status") != InstallmentStatus.CANCELLED]
    if not active:
        return False
    return all(i.get("status") == InstallmentStatus.PAID for i in active)


def should_request_be_completed(quotes: List[Dict]) -> bool:
    """When at least one quote is completed → request completed."""
    if not quotes:
        return False
    return any(q.get("status") == QuoteStatus.COMPLETED for q in quotes)
