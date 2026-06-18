#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP HospiRFQ Processor — Travel & Hospitality MCP Server Facade.

Flat mixin composition: all domain mixins inherit only from
GraphQLBackedProcessor and are composed into this single facade class
that the MCP runtime instantiates.
"""

from __future__ import annotations

__author__ = "Idea Bosque"

import logging
from typing import Any, Dict

from .graphql_backed_processor import GraphQLBackedProcessor
from .request_mixin import RequestMixin
from .item_mixin import ItemMixin
from .availability_mixin import AvailabilityMixin
from .quote_mixin import QuoteMixin
from .pricing_mixin import PricingMixin
from .installment_mixin import InstallmentMixin
from .bundle_mixin import BundleMixin
from .cancellation_mixin import CancellationMixin
from .file_mixin import FileMixin
from .segment_mixin import SegmentMixin
from .catalog_mixin import CatalogMixin


class MCPHospiRFQProcessor(
    RequestMixin,
    ItemMixin,
    AvailabilityMixin,
    QuoteMixin,
    PricingMixin,
    InstallmentMixin,
    BundleMixin,
    CancellationMixin,
    FileMixin,
    SegmentMixin,
    CatalogMixin,
):
    """Public interface aggregating all RFQ and hospitality MCP tools.

    Flat composition replaces the original deep inheritance chain.
    Each mixin contributes its own MCP tool methods and only accesses
    ``self.logger``, ``self.setting``, and ``self._execute_graphql_query``
    (all provided by GraphQLBackedProcessor).  Inter-mixin calls (e.g.
    RequestMixin → QuoteMixin.search_quotes) resolve automatically via
    Python MRO on the facade instance.
    """

    def __init__(self, logger: logging.Logger, **setting: Dict[str, Any]):
        # Explicitly call the root base class to initialise logger, setting,
        # and graphql_client exactly once — mixins only reference these attrs.
        GraphQLBackedProcessor.__init__(self, logger, **setting)