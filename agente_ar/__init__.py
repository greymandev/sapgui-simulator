# agente_ar - LangGraph SAP Tools Module

"""
Agente AR - Asynchronous SAP Tools for LangGraph Integration

This module provides LangGraph-compatible tools for SAP operations:
- fbl5n: Customer line items query (FBL5N transaction)
- cobros: Payment processing (F-28 transaction)

Each tool supports:
- Asynchronous execution
- Optional GUI interface
- Comprehensive logging
- Error handling
- Agent state context

Usage:
    from agente_ar import fbl5n, cobros

    # Query customer items
    result = await fbl5n("123456")

    # Process payment
    result = await cobros("123456", "1800000789", "1250.75")
"""

from .sap_tools import fbl5n, cobros, text_to_json, SAPTools
from .sap_core import SAPCore
from .text_to_json_converter import convert_sap_text_to_json, SAPTextToJSONConverter

__version__ = "1.0.0"
__author__ = "greymandev"

__all__ = [
    "fbl5n",
    "cobros",
    "text_to_json",
    "SAPTools",
    "SAPCore",
    "convert_sap_text_to_json",
    "SAPTextToJSONConverter"
]
