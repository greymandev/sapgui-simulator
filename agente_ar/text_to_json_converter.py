# text_to_json_converter.py - Tool for converting SAP text output to structured JSON

import re
import json
from typing import Dict, Any, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class SAPTextToJSONConverter:
    """Converts SAP text output to structured JSON for LLM consumption"""

    def __init__(self):
        self.patterns = {
            'fbl5n': {
                'header_pattern': r'Customer.*?(\d{6})',
                'item_pattern': r'(\d{10})\s+(\w+(?:\s+\w+)*)\s+(\d{2}\.\d{2}\.\d{4})\s+([-]?\d+(?:,\d{3})*\.\d{2})\s+(\w{3})\s+(\w+(?:\s+\w+)*)',
                'summary_pattern': r'(\d+)\s+items?\s+found',
                'customer_pattern': r'Customer[:\s]+(\d{6})'
            },
            'f28': {
                'header_pattern': r'Payment\s+Processing.*?Customer:\s*(\d{6})',
                'document_pattern': r'Document\s+(\d{10})\s+posted',
                'amount_pattern': r'Amount:\s*([-]?\d+(?:,\d{3})*\.\d{2})\s*(\w{3})',
                'status_pattern': r'Status:\s*(\w+(?:\s+\w+)*)'
            }
        }

    def convert_fbl5n_text_to_json(self, text_data: str) -> Dict[str, Any]:
        """
        Convert FBL5N text output to structured JSON

        Args:
            text_data: Raw text from FBL5N transaction

        Returns:
            Structured JSON with customer line items
        """
        try:
            logger.info("Converting FBL5N text data to JSON")

            # Extract customer ID
            customer_match = re.search(self.patterns['fbl5n']['header_pattern'], text_data)
            customer_id = customer_match.group(1) if customer_match else "Unknown"

            # Extract line items
            items = []
            item_matches = re.finditer(self.patterns['fbl5n']['item_pattern'], text_data)

            for match in item_matches:
                document, doc_type, date, amount, currency, status = match.groups()

                item = {
                    "document_number": document,
                    "document_type": doc_type.strip(),
                    "posting_date": date,
                    "amount": float(amount.replace(',', '')),
                    "currency": currency,
                    "status": status.strip(),
                    "is_open": status.strip().lower() in ['open', 'overdue', 'partially paid']
                }
                items.append(item)

            # Extract summary info
            summary_match = re.search(self.patterns['fbl5n']['summary_pattern'], text_data)
            items_count = int(summary_match.group(1)) if summary_match else len(items)

            # Calculate totals
            total_amount = sum(item['amount'] for item in items)
            open_items = [item for item in items if item['is_open']]
            open_amount = sum(item['amount'] for item in open_items)

            result = {
                "transaction_type": "FBL5N",
                "customer_id": customer_id,
                "query_timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_items": items_count,
                    "open_items": len(open_items),
                    "total_amount": round(total_amount, 2),
                    "open_amount": round(open_amount, 2),
                    "currencies": list(set(item['currency'] for item in items))
                },
                "line_items": items,
                "analysis": {
                    "has_overdue_items": any(item['status'].lower() == 'overdue' for item in items),
                    "largest_open_item": max(open_items, key=lambda x: x['amount']) if open_items else None,
                    "payment_recommendation": "Process oldest overdue items first" if any(item['status'].lower() == 'overdue' for item in items) else "All items current"
                },
                "conversion_status": "success"
            }

            logger.info(f"Successfully converted FBL5N data: {len(items)} items processed")
            return result

        except Exception as e:
            logger.error(f"Failed to convert FBL5N text: {e}")
            return {
                "transaction_type": "FBL5N",
                "conversion_status": "error",
                "error": str(e),
                "raw_text": text_data[:500] + "..." if len(text_data) > 500 else text_data
            }

    def convert_f28_text_to_json(self, text_data: str) -> Dict[str, Any]:
        """
        Convert F-28 payment text output to structured JSON

        Args:
            text_data: Raw text from F-28 transaction

        Returns:
            Structured JSON with payment processing results
        """
        try:
            logger.info("Converting F-28 text data to JSON")

            # Extract customer ID
            customer_match = re.search(self.patterns['f28']['header_pattern'], text_data)
            customer_id = customer_match.group(1) if customer_match else "Unknown"

            # Extract payment document
            doc_match = re.search(self.patterns['f28']['document_pattern'], text_data)
            payment_document = doc_match.group(1) if doc_match else None

            # Extract amount and currency
            amount_match = re.search(self.patterns['f28']['amount_pattern'], text_data)
            amount = float(amount_match.group(1).replace(',', '')) if amount_match else 0.0
            currency = amount_match.group(2) if amount_match else "EUR"

            # Extract status
            status_match = re.search(self.patterns['f28']['status_pattern'], text_data)
            status = status_match.group(1) if status_match else "Unknown"

            # Determine success
            is_successful = "success" in status.lower() or payment_document is not None

            result = {
                "transaction_type": "F-28",
                "customer_id": customer_id,
                "processing_timestamp": datetime.now().isoformat(),
                "payment_details": {
                    "payment_document": payment_document,
                    "amount": amount,
                    "currency": currency,
                    "status": status,
                    "is_successful": is_successful
                },
                "business_impact": {
                    "customer_balance_reduced": amount if is_successful else 0,
                    "document_cleared": is_successful,
                    "posting_complete": is_successful
                },
                "next_actions": [
                    "Verify posting in customer account" if is_successful else "Review error and retry",
                    "Update customer communication" if is_successful else "Escalate to SAP administrator"
                ],
                "conversion_status": "success"
            }

            logger.info(f"Successfully converted F-28 data: Document {payment_document}")
            return result

        except Exception as e:
            logger.error(f"Failed to convert F-28 text: {e}")
            return {
                "transaction_type": "F-28",
                "conversion_status": "error",
                "error": str(e),
                "raw_text": text_data[:500] + "..." if len(text_data) > 500 else text_data
            }

# LangGraph tool function
async def convert_sap_text_to_json(text_data: str, transaction_type: str, state: Optional[Dict] = None) -> Dict[str, Any]:
    """
    LangGraph tool: Convert SAP text output to structured JSON

    Args:
        text_data: Raw text output from SAP transaction
        transaction_type: Type of transaction ('fbl5n' or 'f28')
        state: Agent state context

    Returns:
        Structured JSON data for LLM consumption
    """
    start_time = datetime.now()
    args = {"text_length": len(text_data), "transaction_type": transaction_type}

    try:
        logger.info(f"🔄 Converting {transaction_type.upper()} text to JSON ({len(text_data)} chars)")

        converter = SAPTextToJSONConverter()

        if transaction_type.lower() == 'fbl5n':
            result = converter.convert_fbl5n_text_to_json(text_data)
        elif transaction_type.lower() == 'f28':
            result = converter.convert_f28_text_to_json(text_data)
        else:
            raise ValueError(f"Unsupported transaction type: {transaction_type}")

        # Add execution metadata
        execution_time = (datetime.now() - start_time).total_seconds()
        result.update({
            "tool_metadata": {
                "execution_time": f"{execution_time:.2f}s",
                "input_size": len(text_data),
                "conversion_timestamp": start_time.isoformat(),
                "agent_state": state or {}
            }
        })

        # Log successful conversion
        logger.info(f"✅ Text conversion successful: {transaction_type} → JSON ({len(str(result))} chars)")

        return result

    except Exception as e:
        error_result = {
            "conversion_status": "error",
            "transaction_type": transaction_type,
            "error": str(e),
            "execution_time": f"{(datetime.now() - start_time).total_seconds():.2f}s",
            "input_preview": text_data[:200] + "..." if len(text_data) > 200 else text_data
        }
        logger.error(f"❌ Text conversion failed: {e}")
        return error_result
