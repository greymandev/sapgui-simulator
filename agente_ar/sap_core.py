# sap_core.py - Core business logic for SAP operations

import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SAPCore:
    """Core SAP business logic without GUI dependencies"""

    def __init__(self):
        self.company_code = "1000"

    def process_payment(self, customer: str, doc_num: str, amount: str) -> Dict[str, Any]:
        """
        Core F-28 payment processing logic

        Args:
            customer: Customer ID (6 digits)
            doc_num: Document number to clear
            amount: Payment amount

        Returns:
            Dict with processing result
        """
        try:
            logger.info(f"Processing payment for customer {customer}, doc: {doc_num}, amount: {amount}")

            # Validate inputs
            if not customer or not customer.isdigit() or len(customer) != 6:
                raise ValueError(f"Invalid customer ID: {customer}")

            if not doc_num or not doc_num.isdigit():
                raise ValueError(f"Invalid document number: {doc_num}")

            if not amount:
                raise ValueError("Amount is required")

            # Simulate processing time
            time.sleep(1)

            # Generate payment document
            payment_doc = random.randint(1400000000, 1499999999)

            result = {
                "status": "success",
                "message": f"Payment processed successfully. Document {payment_doc} posted in company {self.company_code}",
                "payment_document": str(payment_doc),
                "customer_id": customer,
                "cleared_document": doc_num,
                "amount": amount,
                "company_code": self.company_code,
                "posting_date": datetime.now().strftime("%d.%m.%Y"),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Payment processing completed: {result}")
            return result

        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"Payment processing failed: {str(e)}",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Payment processing error: {error_result}")
            return error_result

    def query_customer_items(self, customer_id: str) -> Dict[str, Any]:
        """
        Core FBL5N customer line items query logic

        Args:
            customer_id: Customer ID to query

        Returns:
            Dict with query results
        """
        try:
            logger.info(f"Querying customer line items for: {customer_id}")

            # Validate input
            if not customer_id or not customer_id.isdigit() or len(customer_id) != 6:
                raise ValueError(f"Invalid customer ID: {customer_id}")

            # Simulate processing time
            time.sleep(1)

            # Generate sample data
            doc_types = ['Invoice', 'Credit Memo', 'Payment', 'Debit Memo']
            currencies = ['EUR', 'USD', 'GBP']
            statuses = ['Open', 'Partially Paid', 'Overdue']

            items = []
            num_items = random.randint(3, 8)

            for i in range(num_items):
                doc_num = f"180000{random.randint(1000, 9999)}"
                doc_type = random.choice(doc_types)

                # Random date within last 90 days
                days_ago = random.randint(1, 90)
                doc_date = (datetime.now() - timedelta(days=days_ago)).strftime("%d.%m.%Y")

                # Random amount
                if doc_type == 'Credit Memo':
                    amount = f"-{random.randint(100, 5000):.2f}"
                else:
                    amount = f"{random.randint(500, 10000):.2f}"

                currency = random.choice(currencies)
                status = random.choice(statuses)

                item = {
                    "document": doc_num,
                    "doc_type": doc_type,
                    "date": doc_date,
                    "amount": amount,
                    "currency": currency,
                    "status": status
                }
                items.append(item)

            result = {
                "status": "success",
                "message": f"Found {len(items)} open items for customer {customer_id}",
                "customer_id": customer_id,
                "company_code": self.company_code,
                "items_count": len(items),
                "items": items,
                "query_date": datetime.now().strftime("%d.%m.%Y"),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"Customer query completed: {len(items)} items found")
            return result

        except Exception as e:
            error_result = {
                "status": "error",
                "message": f"Customer query failed: {str(e)}",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"Customer query error: {error_result}")
            return error_result
