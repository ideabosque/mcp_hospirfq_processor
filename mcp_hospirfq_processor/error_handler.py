#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centralized error handling module for MCP HospiRFQ Processor.

Extends the base mcp_rfq_processor error handler with hospitality-specific
error codes for availability holds, bundles, cancellation policies, and
catalog search.
"""

from __future__ import annotations

__author__ = "Idea Bosque"

import re
import traceback
from functools import wraps
from typing import Any, Callable, Dict, Optional


# ==================== Error Code Constants ====================


class ErrorCode:
    """Error codes for programmatic error handling."""

    # GraphQL/API Errors
    GRAPHQL_QUERY_FAILED = "GRAPHQL_QUERY_FAILED"
    GRAPHQL_SCHEMA_FETCH_FAILED = "GRAPHQL_SCHEMA_FETCH_FAILED"
    API_CONNECTION_FAILED = "API_CONNECTION_FAILED"

    # Validation Errors
    VALIDATION_FAILED = "VALIDATION_FAILED"
    ITEM_NOT_FOUND = "ITEM_NOT_FOUND"
    NO_ITEMS_FOUND = "NO_ITEMS_FOUND"
    INVALID_ARGUMENTS = "INVALID_ARGUMENTS"
    MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"

    # General Errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    OPERATION_FAILED = "OPERATION_FAILED"

    # Hospitality-Specific Errors — Availability Holds
    HOLD_NOT_FOUND = "HOLD_NOT_FOUND"
    HOLD_ALREADY_CONFIRMED = "HOLD_ALREADY_CONFIRMED"
    HOLD_ALREADY_RELEASED = "HOLD_ALREADY_RELEASED"
    HOLD_ALREADY_EXPIRED = "HOLD_ALREADY_EXPIRED"
    AVAILABILITY_CHECK_FAILED = "AVAILABILITY_CHECK_FAILED"
    AVAILABILITY_INSUFFICIENT = "AVAILABILITY_INSUFFICIENT"
    BATCH_NOT_QUANTIFIED = "BATCH_NOT_QUANTIFIED"

    # Hospitality-Specific Errors — Bundle / Cancellation / Catalog
    BUNDLE_NOT_FOUND = "BUNDLE_NOT_FOUND"
    CANCEL_POLICY_NOT_FOUND = "CANCEL_POLICY_NOT_FOUND"
    CATALOG_SEARCH_FAILED = "CATALOG_SEARCH_FAILED"

    # Hospitality-Specific Errors — Pricing
    PRICING_MODE_UNSUPPORTED = "PRICING_MODE_UNSUPPORTED"
    PAX_BREAKDOWN_MISMATCH = "PAX_BREAKDOWN_MISMATCH"


# ==================== Custom Exception Classes ====================


class MCPError(Exception):
    """Base exception class for MCP HospiRFQ Processor errors."""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.UNKNOWN_ERROR,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class GraphQLError(MCPError):
    """Exception raised for GraphQL-related errors."""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.GRAPHQL_QUERY_FAILED,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, error_code, details)


class ValidationError(MCPError):
    """Exception raised for validation errors."""

    def __init__(
        self,
        message: str,
        error_code: str = ErrorCode.VALIDATION_FAILED,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, error_code, details)


# ==================== Error Message Extraction ====================


def extract_error_message(error_str: str) -> str:
    """Extract clean error message from GraphQL error response."""
    try:
        message_match = re.search(r"'message':\s*\"([^\"]+)\"", error_str)
        if not message_match:
            message_match = re.search(r"'message':\s*'([^']+)'", error_str)
        if message_match:
            return message_match.group(1)
        return str(error_str)
    except Exception:
        return str(error_str)


# ==================== Error Response Builders ====================


def build_error_response(
    message: str,
    error_code: str = ErrorCode.UNKNOWN_ERROR,
    details: Optional[Dict[str, Any]] = None,
    include_code: bool = True,
) -> Dict[str, Any]:
    """Build standardized error response dictionary."""
    response = {"error": message}
    if include_code:
        response["error_code"] = error_code
    if details:
        response["details"] = details
    return response


def build_error_from_exception(
    exception: Exception, include_code: bool = True
) -> Dict[str, Any]:
    """Build error response from an exception instance."""
    if isinstance(exception, MCPError):
        return build_error_response(
            message=exception.message,
            error_code=exception.error_code,
            details=exception.details,
            include_code=include_code,
        )
    else:
        clean_message = extract_error_message(str(exception))
        return build_error_response(
            message=clean_message,
            error_code=ErrorCode.UNKNOWN_ERROR,
            include_code=include_code,
        )


# ==================== Error Handler Decorator ====================


def handle_errors(
    operation_name: str, log_traceback: bool = False, include_error_code: bool = True
) -> Callable:
    """Decorator for consistent error handling across MCP methods."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Dict[str, Any]:
            try:
                result = func(self, *args, **kwargs)
                if isinstance(result, dict) and "error" in result:
                    if include_error_code and "error_code" not in result:
                        result["error_code"] = ErrorCode.OPERATION_FAILED
                return result
            except MCPError as e:
                if log_traceback:
                    log = traceback.format_exc()
                    self.logger.error(log)
                else:
                    self.logger.error(f"Failed to {operation_name}: {e.message}")
                return build_error_from_exception(e, include_error_code)
            except Exception as e:
                if log_traceback:
                    log = traceback.format_exc()
                    self.logger.error(log)
                else:
                    self.logger.error(f"Failed to {operation_name}: {e}")
                return build_error_from_exception(e, include_error_code)

        return wrapper

    return decorator


# ==================== Validation Utilities ====================


def validate_not_empty(
    value: Any, field_name: str, error_message: Optional[str] = None
) -> None:
    """Validate that a value is not empty. Raises ValidationError otherwise."""
    if not value:
        message = error_message or f"{field_name} cannot be empty"
        raise ValidationError(
            message=message,
            error_code=(
                ErrorCode.NO_ITEMS_FOUND
                if "items" in field_name.lower()
                else ErrorCode.VALIDATION_FAILED
            ),
            details={"field": field_name},
        )


def propagate_error_if_present(result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Check if result contains an error and return it if present."""
    if isinstance(result, dict) and "error" in result:
        return result
    return None