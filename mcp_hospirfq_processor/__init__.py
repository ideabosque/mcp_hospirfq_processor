#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MCP HospiRFQ Processor — Travel & Hospitality MCP Server."""

from __future__ import annotations

__author__ = "Idea Bosque"
__version__ = "0.1.0"

from .mcp_hospirfq_processor import MCPHospiRFQProcessor
from .mcp_configuration import MCP_CONFIGURATION

__all__ = ["MCPHospiRFQProcessor", "MCP_CONFIGURATION"]