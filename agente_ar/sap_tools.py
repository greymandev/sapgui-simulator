# sap_tools.py - LangGraph tools for SAP operations

import asyncio
import threading
import time
import sys
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from sap_core import SAPCore
from sap_text_generator import SAPTextGenerator
from text_to_json_converter import convert_sap_text_to_json

# Import macOS GUI manager from parent directory
sys.path.append('..')
try:
    from macos_gui_manager import gui_thread_safe, is_gui_safe, get_safe_gui_mode
except ImportError:
    # Fallback if manager not available
    def gui_thread_safe(func):
        return func
    def is_gui_safe():
        return True
    def get_safe_gui_mode():
        return 'gui'

# Configure logging
logger = logging.getLogger(__name__)

class SAPTools:
    """SAP Tools for LangGraph integration with optional GUI support"""

    def __init__(self):
        self.core = SAPCore()
        self.text_generator = SAPTextGenerator()
        self._gui_windows = {}

    def log_tool_execution(self, tool_name: str, args: Dict[str, Any], result: Dict[str, Any], state: Optional[Dict] = None):
        """Log tool execution with required information"""
        log_entry = {
            "tool_name": tool_name,
            "timestamp": datetime.now().isoformat(),
            "input_args": args,
            "output_result": {
                "status": result.get("status"),
                "message": result.get("message"),
                "data_summary": f"{len(result.get('items', []))} items" if 'items' in result else "N/A"
            },
            "state_context": state or {},
            "execution_time": result.get("execution_time", "N/A")
        }

        if result.get("status") == "error":
            logger.error(f"Tool execution failed: {log_entry}")
        else:
            logger.info(f"Tool execution successful: {log_entry}")

        return log_entry

    async def process_payment_tool(self, customer: str, doc_num: str, amount: str, with_gui: bool = True, state: Optional[Dict] = None) -> Dict[str, Any]:
        """
        LangGraph tool for F-28 payment processing with GUI and text export

        Args:
            customer: Customer ID (6 digits)
            doc_num: Document number to clear
            amount: Payment amount
            with_gui: Whether to show GUI (default: True, auto-detects safety)
            state: Current agent state context

        Returns:
            Dict with processing result, GUI data, and text export
        """
        start_time = time.time()

        # Auto-detect safe GUI mode on macOS
        safe_gui_mode = get_safe_gui_mode()
        if with_gui and safe_gui_mode == 'headless':
            logger.warning("🚨 GUI requested but not safe on current thread. Switching to headless mode.")
            with_gui = False

        args = {"customer": customer, "doc_num": doc_num, "amount": amount, "with_gui": with_gui, "auto_mode": safe_gui_mode}

        try:
            logger.info(f"🚀 Executing process_payment_tool with args: {args}")

            # Execute core business logic
            core_result = self.core.process_payment(customer, doc_num, amount)
            core_result["execution_time"] = f"{time.time() - start_time:.2f}s"

            # Generate SAP-like text output (always, as in real SAP)
            text_output = None
            if core_result["status"] == "success":
                text_output = self.text_generator.generate_f28_text_output(
                    customer, doc_num, amount, core_result["payment_document"]
                )
                # Simulate clipboard export
                clipboard_text = self.text_generator.simulate_clipboard_export(text_output)

            # If GUI requested, launch it asynchronously
            gui_data = None
            if with_gui and core_result["status"] == "success":
                gui_data = await self._launch_payment_gui(customer, doc_num, amount)

            # Prepare final result
            result = {
                **core_result,
                "gui_launched": with_gui and gui_data is not None,
                "gui_data": gui_data,
                "text_export": {
                    "sap_output": text_output,
                    "clipboard_content": clipboard_text if text_output else None,
                    "export_available": text_output is not None
                },
                "tool_type": "payment_processing"
            }

            # Log execution
            self.log_tool_execution("process_payment_tool", args, result, state)

            return result

        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}",
                "error": str(e),
                "execution_time": f"{time.time() - start_time:.2f}s",
                "tool_type": "payment_processing"
            }
            self.log_tool_execution("process_payment_tool", args, error_result, state)
            return error_result

    async def query_customer_items_tool(self, customer_id: str, with_gui: bool = True, state: Optional[Dict] = None) -> Dict[str, Any]:
        """
        LangGraph tool for FBL5N customer line items query with GUI and text export

        Args:
            customer_id: Customer ID to query
            with_gui: Whether to show GUI (default: True, auto-detects safety)
            state: Current agent state context

        Returns:
            Dict with query results, GUI data, and text export
        """
        start_time = time.time()

        # Auto-detect safe GUI mode on macOS
        safe_gui_mode = get_safe_gui_mode()
        if with_gui and safe_gui_mode == 'headless':
            logger.warning("🚨 GUI requested but not safe on current thread. Switching to headless mode.")
            with_gui = False

        args = {"customer_id": customer_id, "with_gui": with_gui, "auto_mode": safe_gui_mode}

        try:
            logger.info(f"🔍 Executing query_customer_items_tool with args: {args}")

            # Execute core business logic
            core_result = self.core.query_customer_items(customer_id)
            core_result["execution_time"] = f"{time.time() - start_time:.2f}s"

            # Generate SAP-like text output (always, as in real SAP)
            text_output = None
            if core_result["status"] == "success":
                text_output = self.text_generator.generate_fbl5n_text_output(
                    customer_id, core_result["items"]
                )
                # Simulate clipboard export
                clipboard_text = self.text_generator.simulate_clipboard_export(text_output)

            # If GUI requested, launch it asynchronously
            gui_data = None
            if with_gui and core_result["status"] == "success":
                gui_data = await self._launch_query_gui(customer_id, core_result["items"])

            # Prepare final result
            result = {
                **core_result,
                "gui_launched": with_gui and gui_data is not None,
                "gui_data": gui_data,
                "text_export": {
                    "sap_output": text_output,
                    "clipboard_content": clipboard_text if text_output else None,
                    "export_available": text_output is not None
                },
                "tool_type": "customer_query"
            }

            # Log execution
            self.log_tool_execution("query_customer_items_tool", args, result, state)

            return result

        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"Tool execution failed: {str(e)}",
                "error": str(e),
                "execution_time": f"{time.time() - start_time:.2f}s",
                "tool_type": "customer_query"
            }
            self.log_tool_execution("query_customer_items_tool", args, error_result, state)
            return error_result

    async def _launch_payment_gui(self, customer: str, doc_num: str, amount: str) -> Optional[Dict[str, Any]]:
        """Launch F-28 GUI with macOS thread safety"""
        try:
            # Check if GUI is safe to launch
            if not is_gui_safe():
                logger.warning("GUI not safe on current thread, skipping GUI launch")
                return {
                    "gui_launched": False,
                    "reason": "GUI unsafe on non-main thread",
                    "recommendation": "Use headless mode"
                }

            # Import GUI function with thread safety
            from payment_gui_tool import launch_payment_gui

            # Create thread-safe wrapper
            @gui_thread_safe
            def safe_launch():
                return launch_payment_gui(customer, doc_num, amount)

            # Execute in thread pool but with safety wrapper
            loop = asyncio.get_event_loop()
            gui_data = await loop.run_in_executor(None, safe_launch)
            return gui_data

        except Exception as e:
            logger.error(f"Failed to launch payment GUI: {e}")
            if "NSWindow" in str(e) or "main thread" in str(e):
                logger.error("macOS GUI threading issue detected. Consider using headless mode.")
            return {
                "gui_launched": False,
                "error": str(e),
                "recommendation": "Use with_gui=False for headless operation"
            }

    async def _launch_query_gui(self, customer_id: str, items: list) -> Optional[Dict[str, Any]]:
        """Launch FBL5N GUI with macOS thread safety"""
        try:
            # Check if GUI is safe to launch
            if not is_gui_safe():
                logger.warning("GUI not safe on current thread, skipping GUI launch")
                return {
                    "gui_launched": False,
                    "reason": "GUI unsafe on non-main thread",
                    "recommendation": "Use headless mode"
                }

            # Import GUI function with thread safety
            from query_gui_tool import launch_query_gui

            # Create thread-safe wrapper
            @gui_thread_safe
            def safe_launch():
                return launch_query_gui(customer_id, items)

            # Execute in thread pool but with safety wrapper
            loop = asyncio.get_event_loop()
            gui_data = await loop.run_in_executor(None, safe_launch)
            return gui_data

        except Exception as e:
            logger.error(f"Failed to launch query GUI: {e}")
            if "NSWindow" in str(e) or "main thread" in str(e):
                logger.error("macOS GUI threading issue detected. Consider using headless mode.")
            return {
                "gui_launched": False,
                "error": str(e),
                "recommendation": "Use with_gui=False for headless operation"
            }
        except Exception as e:
            logger.error(f"Failed to launch query GUI: {e}")
            return None

# Convenience functions for direct LangGraph integration
sap_tools = SAPTools()

async def fbl5n(customer_id: str, with_gui: bool = True, state: Optional[Dict] = None) -> Dict[str, Any]:
    """
    LangGraph tool function: Query customer line items (FBL5N)

    Usage: fbl5n("123456")
    """
    return await sap_tools.query_customer_items_tool(customer_id, with_gui, state)

async def cobros(customer: str, doc_num: str, amount: str, with_gui: bool = True, state: Optional[Dict] = None) -> Dict[str, Any]:
    """
    LangGraph tool function: Process payment (F-28)

    Usage: cobros("123456", "1800000789", "1250.75")
    """
    return await sap_tools.process_payment_tool(customer, doc_num, amount, with_gui, state)

async def text_to_json(text_data: str, transaction_type: str, state: Optional[Dict] = None) -> Dict[str, Any]:
    """
    LangGraph tool function: Convert SAP text output to structured JSON

    Usage: text_to_json(sap_text_output, "fbl5n")
    """
    return await convert_sap_text_to_json(text_data, transaction_type, state)
