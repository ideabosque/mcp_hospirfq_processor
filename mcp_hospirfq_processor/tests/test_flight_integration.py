#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flight integration tests — verify flight domain patterns work through the
same 38 MCP tools using item_type, pricing_mode, and batch_no conventions.

These tests mock _execute_graphql_query but exercise the full call chain
through the facade class to verify that:
1. Flights use the same tools as hotels (no separate flight MCP tools)
2. batch_no encodes flight number + date (e.g., AF1234-20260815)
3. pricing_mode="per_pax_type" with pax_breakdown
4. uom="seat" for flight items
5. availability_mode="require_hold" for flights
6. bundle_type="flight_itinerary" for multi-leg flight bundles
7. Cancellation policies use hours_before_departure_gte tiers
"""

from __future__ import annotations

__author__ = "Idea Bosque"

import json
import logging

import pytest

logger = logging.getLogger("test_mcp_hospirfq_processor")


# ============================================================================
# Flight Item Submission — same submit_rfq_request tool
# ============================================================================


class TestFlightItemSubmission:
    """Flights are submitted as items via the same request flow."""

    @pytest.mark.unit
    def test_flight_item_in_request(self, processor):
        """A flight item uses item_type='flight' and uom='seat'."""
        processor._execute_graphql_query.return_value = {
            "request": {
                "requestUuid": "req-flight-001",
                "status": "initial",
                "items": [
                    {
                        "itemUuid": "i-flight-1",
                        "itemType": "flight",
                        "itemName": "AF1234 CDG→JFK 2026-08-15",
                        "uom": "seat",
                        "qty": 3,
                    }
                ],
            }
        }
        result = processor.submit_rfq_request(
            email="agent@travel.com",
            request_title="Flight inquiry: Paris to New York",
        )
        assert "error" not in result
        assert result["status"] == "initial"
        assert result["items"][0]["item_type"] == "flight"
        assert result["items"][0]["uom"] == "seat"


# ============================================================================
# Flight Availability Hold — availability_mode=require_hold
# ============================================================================


class TestFlightAvailabilityHold:
    """Flights require availability holds (availability_mode='require_hold')."""

    @pytest.mark.unit
    def test_acquire_flight_hold_with_pax_breakdown(self, processor):
        """Flight hold includes pax_breakdown for adult/child/infant."""
        processor._execute_graphql_query.return_value = {
            "holdToken": "flight-hold-001",
            "status": "held",
            "expiresAt": "2026-08-14T18:30:00Z",
        }
        result = processor.acquire_availability_hold(
            partition_key="AIRLINE-AF",
            provider_item_uuid="pi-flight-af1234",
            service_start_at="2026-08-15T10:00:00Z",
            service_end_at="2026-08-15T13:00:00Z",
            qty=3,
            batch_no="AF1234-20260815",
            pax_breakdown={"adult": 2, "child": 1, "infant": 0},
        )
        assert "error" not in result
        assert result["hold_token"] == "flight-hold-001"
        assert result["status"] == "held"

        # Verify batch_no encodes flight number + date
        variables = processor._execute_graphql_query.call_args[0][3]
        assert variables["batchNo"] == "AF1234-20260815"
        assert variables["paxBreakdown"]["adult"] == 2

    @pytest.mark.unit
    def test_check_flight_availability(self, processor):
        """Check available seats on a flight leg."""
        processor._execute_graphql_query.return_value = {
            "availableQty": 12,
            "serviceStartAt": "2026-08-15T10:00:00Z",
            "serviceEndAt": "2026-08-15T13:00:00Z",
        }
        result = processor.check_availability(
            partition_key="AIRLINE-AF",
            provider_item_uuid="pi-flight-af1234",
            service_start_at="2026-08-15T10:00:00Z",
            service_end_at="2026-08-15T13:00:00Z",
            batch_no="AF1234-20260815",
        )
        assert result["available_qty"] == 12

    @pytest.mark.unit
    def test_confirm_then_release_flight_hold(self, processor):
        """Hold can be confirmed (booking) or released (cancellation)."""
        # Step 1: Confirm
        processor._execute_graphql_query.return_value = {
            "holdToken": "fh-1", "status": "confirmed",
        }
        result = processor.confirm_availability_hold(
            partition_key="AIRLINE-AF", hold_token="fh-1",
            provider_item_uuid="pi-flight-af1234",
        )
        assert result["status"] == "confirmed"

        # Step 2: Released hold stays released (idempotent)
        processor._execute_graphql_query.return_value = {
            "holdToken": "fh-2", "status": "released",
        }
        result = processor.release_availability_hold(
            partition_key="AIRLINE-AF", hold_token="fh-2",
            provider_item_uuid="pi-flight-af1234",
        )
        assert result["status"] == "released"


# ============================================================================
# Flight Pricing — pricing_mode=per_pax_type
# ============================================================================


class TestFlightPricing:
    """Flights use per_pax_type pricing with adult/child/infant rates."""

    @pytest.mark.unit
    def test_flight_price_tiers(self, processor):
        """Flight price tiers return per-pax-type breakdown."""
        processor._execute_graphql_query.return_value = [
            {
                "itemUuid": "i-flight-1",
                "providerItemUuid": "pi-af1234",
                "itemPriceTierUuid": "tier-1",
                "quantityGreaterThen": 1,
                "quantityLessThen": 10,
                "pricePerUom": 850.00,
                "marginPerUom": 50.00,
                "status": "active",
            },
        ]
        result = processor.get_item_price_tiers(
            email="agent@travel.com",
            quote_items=[
                {"item_uuid": "i-flight-1", "provider_item_uuid": "pi-af1234", "qty": 3},
            ],
        )
        assert "error" not in result
        # Result is wrapped: {"item_price_tiers": [...]}
        assert "item_price_tiers" in result
        tiers = result["item_price_tiers"]
        assert len(tiers) >= 1
        assert tiers[0]["price_per_uom"] == 850.00


# ============================================================================
# Flight Itinerary Bundles — bundle_type=flight_itinerary
# ============================================================================


class TestFlightItineraryBundle:
    """Multi-leg flights use bundle_type='flight_itinerary'."""

    @pytest.mark.unit
    def test_search_flight_itinerary_bundles(self, processor):
        """Search for flight itinerary bundles."""
        processor._execute_graphql_query.return_value = [
            {
                "bundleUuid": "b-itin-1",
                "bundleCode": "CDG-JFK-LAX-RT",
                "bundleType": "itinerary",
                "status": "active",
            }
        ]
        result = processor.search_bundles(
            partition_key="AIRLINE-AF",
            bundle_type="itinerary",
        )
        assert "error" not in result
        assert result[0]["bundle_type"] == "itinerary"

    @pytest.mark.unit
    def test_get_flight_itinerary_with_components(self, processor):
        """A flight itinerary bundle has flight leg components."""
        processor._execute_graphql_query.return_value = {
            "bundleUuid": "b-itin-1",
            "bundleCode": "CDG-JFK-LAX-RT",
            "bundleType": "itinerary",
            "components": [
                {"componentUuid": "c-leg1", "itemType": "flight", "batchNo": "AF1234-20260815", "qty": 3},
                {"componentUuid": "c-leg2", "itemType": "flight", "batchNo": "AF5678-20260822", "qty": 3},
            ],
        }
        result = processor.get_bundle(
            partition_key="AIRLINE-AF",
            bundle_uuid="b-itin-1",
        )
        assert "error" not in result
        assert len(result["components"]) == 2
        # Both components are flights
        assert all(c["item_type"] == "flight" for c in result["components"])


# ============================================================================
# Flight Cancellation — hours_before_departure_gte tiers
# ============================================================================


class TestFlightCancellationPolicies:
    """Flight cancellation uses hours_before_service_gte (= departure time)."""

    @pytest.mark.unit
    def test_flight_cancellation_tiers(self, processor):
        """Flight cancellation policy has hours-based tiers."""
        processor._execute_graphql_query.return_value = {
            "policyUuid": "pol-flight-1",
            "providerItemUuid": "pi-af1234",
            "tiers": [
                {"hoursBeforeServiceGte": 168, "refundPercentage": 100, "description": "Free cancellation 7+ days"},
                {"hoursBeforeServiceGte": 24, "refundPercentage": 50, "description": "50% refund 1-7 days"},
                {"hoursBeforeServiceGte": 0, "refundPercentage": 0, "description": "No refund < 24h"},
            ],
        }
        result = processor.get_cancellation_policy(
            partition_key="AIRLINE-AF",
            policy_uuid="pol-flight-1",
        )
        assert "error" not in result
        assert result["policy_uuid"] == "pol-flight-1"
        assert len(result["tiers"]) == 3
        # First tier: 168 hours = 7 days
        assert result["tiers"][0]["hours_before_service_gte"] == 168
        assert result["tiers"][0]["refund_percentage"] == 100

    @pytest.mark.unit
    def test_search_flight_cancellation_policies(self, processor):
        """Search cancellation policies for a specific flight provider item."""
        processor._execute_graphql_query.return_value = [
            {"policyUuid": "pol-flight-1", "status": "active"},
        ]
        result = processor.search_cancellation_policies(
            partition_key="AIRLINE-AF",
            provider_item_uuid="pi-af1234",
        )
        assert "error" not in result
        assert len(result) == 1


# ============================================================================
# Cross-Domain — Flight + Hotel Combined
# ============================================================================


class TestFlightHotelCombined:
    """Verify flight and hotel items coexist in the same request."""

    @pytest.mark.unit
    def test_mixed_flight_hotel_request(self, processor):
        """A single request can contain both flight and hotel items."""
        processor._execute_graphql_query.return_value = {
            "requestUuid": "req-combined-001",
            "status": "confirmed",
            "items": [
                {
                    "itemUuid": "i-flight-1",
                    "itemType": "flight",
                    "itemName": "AF1234 CDG→JFK",
                    "uom": "seat",
                    "qty": 2,
                    "pricingMode": "per_pax_type",
                },
                {
                    "itemUuid": "i-hotel-1",
                    "itemType": "hotel_room",
                    "itemName": "Marriott Times Square - Deluxe",
                    "uom": "room_night",
                    "qty": 3,
                    "pricingMode": "occupancy",
                },
            ],
        }
        result = processor.get_rfq_request(request_uuid="req-combined-001")
        assert "error" not in result
        items = result["items"]
        assert len(items) == 2
        flight_item = next(i for i in items if i["item_type"] == "flight")
        hotel_item = next(i for i in items if i["item_type"] == "hotel_room")
        assert flight_item["uom"] == "seat"
        assert hotel_item["uom"] == "room_night"
        assert flight_item["pricing_mode"] == "per_pax_type"
        assert hotel_item["pricing_mode"] == "occupancy"


# ============================================================================
# Catalog — Flight Search
# ============================================================================


class TestFlightCatalogInquiry:
    """KGE catalog search works for flight products too."""

    @pytest.mark.unit
    def test_inquire_flight_catalog(self, processor):
        """Search catalog for flights using namespace filter."""
        processor._execute_graphql_query.return_value = [
            {"itemUuid": "i-af1234", "itemName": "Air France AF1234 CDG→JFK", "score": 0.98},
            {"itemUuid": "i-ba178", "itemName": "British Airways BA178 LHR→JFK", "score": 0.91},
        ]
        result = processor.inquire_catalog(
            partition_key="AIRLINE-AF",
            query_text="paris to new york",
            namespace="flights",
            limit=5,
        )
        assert "error" not in result
        assert len(result) == 2
        assert result[0]["score"] == 0.98