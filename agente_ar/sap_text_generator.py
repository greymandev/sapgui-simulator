# sap_text_generator.py - Generate SAP-like text output for realistic simulation

import random
from datetime import datetime, timedelta
from typing import Dict, Any, List

class SAPTextGenerator:
    """Generate realistic SAP text output that mimics real SAP system exports"""

    def generate_fbl5n_text_output(self, customer_id: str, items: List[Dict[str, Any]]) -> str:
        """
        Generate FBL5N text output that looks like real SAP export

        Args:
            customer_id: Customer ID
            items: List of line items

        Returns:
            Formatted text resembling SAP FBL5N output
        """
        current_date = datetime.now().strftime("%d.%m.%Y")
        current_time = datetime.now().strftime("%H:%M:%S")

        # Header section
        text_output = f"""
================================================================================
                           Customer Line Items - FBL5N
================================================================================
Run Date: {current_date}                                        Time: {current_time}
User: SAPUSER                                             Client: 100
Company Code: 1000                                        Customer: {customer_id}

Selection Criteria:
  Company Code........: 1000
  Customer............: {customer_id}
  Open Items Only.....: X
  Date From...........: {(datetime.now() - timedelta(days=90)).strftime("%d.%m.%Y")}
  Date To.............: {current_date}

================================================================================
Document    Doc Type      Date        Amount        Curr  Status
================================================================================
"""

        # Items section
        total_amount = 0
        for item in items:
            doc_num = item.get('document', '0000000000')
            doc_type = item.get('doc_type', 'Invoice').ljust(12)
            date = item.get('date', current_date)
            amount = float(item.get('amount', '0').replace('-', '').replace(',', ''))
            currency = item.get('currency', 'EUR')
            status = item.get('status', 'Open').ljust(10)

            # Format amount with proper alignment
            amount_str = f"{amount:>12,.2f}"
            if item.get('amount', '').startswith('-'):
                amount_str = f"-{amount:>11,.2f}"

            text_output += f"{doc_num}  {doc_type}  {date}  {amount_str}  {currency}   {status}\n"
            total_amount += amount if not item.get('amount', '').startswith('-') else -amount

        # Footer section
        text_output += f"""
================================================================================
Summary:
  Total Items Found...: {len(items)}
  Total Amount........: {total_amount:>12,.2f} EUR
  Open Items..........: {len([i for i in items if i.get('status', '').lower() in ['open', 'overdue']])}

Report Generation Complete.
Processing Time: 0.847 seconds
================================================================================
"""

        return text_output.strip()

    def generate_f28_text_output(self, customer_id: str, doc_num: str, amount: str, payment_doc: str) -> str:
        """
        Generate F-28 payment processing text output

        Args:
            customer_id: Customer ID
            doc_num: Document being cleared
            amount: Payment amount
            payment_doc: Generated payment document

        Returns:
            Formatted text resembling SAP F-28 output
        """
        current_date = datetime.now().strftime("%d.%m.%Y")
        current_time = datetime.now().strftime("%H:%M:%S")

        text_output = f"""
================================================================================
                        Payment Processing - F-28
================================================================================
Processing Date: {current_date}                               Time: {current_time}
User: SAPUSER                                            Session: 001
Company Code: 1000                                       Customer: {customer_id}

Payment Header:
  Document Date.......: {current_date}
  Posting Date........: {current_date}
  Company Code........: 1000
  Document Type.......: DZ (Payment)
  Reference...........: AUTO_PAYMENT_{payment_doc}

Customer Information:
  Customer ID.........: {customer_id}
  Customer Name.......: Customer Demo Ltd.
  Payment Terms.......: Net 30

Document Selection:
  Document Number.....: {doc_num}
  Amount..............: {amount} EUR
  Document Type.......: Invoice
  Status..............: Open → Cleared

================================================================================
PAYMENT PROCESSING RESULTS:
================================================================================

✓ Document Validation: PASSED
✓ Customer Check: PASSED
✓ Amount Verification: PASSED
✓ Posting Authorization: PASSED

Payment Document: {payment_doc}
Status: SUCCESS - Document posted successfully

Cleared Items:
  {doc_num} ................. {amount} EUR

New Documents Created:
  {payment_doc} ................. {amount} EUR (Payment)

Account Postings:
  Customer Account {customer_id} ......... CREDIT {amount} EUR
  Bank Clearing Account .................. DEBIT  {amount} EUR

================================================================================
Processing Summary:
  Documents Processed.: 1
  Amount Posted.......: {amount} EUR
  Status..............: SUCCESS

Processing Time: 1.234 seconds
Transaction Complete: {current_time}
================================================================================
"""

        return text_output.strip()

    def simulate_clipboard_export(self, text_data: str) -> str:
        """
        Simulate what would be copied to clipboard from SAP

        Args:
            text_data: Original SAP text output

        Returns:
            Cleaned text as if copied from SAP GUI
        """
        # Simulate clipboard formatting (remove some formatting characters)
        clipboard_text = text_data.replace("================================================================================", "")
        clipboard_text = clipboard_text.replace("✓", "[OK]")

        # Add clipboard metadata
        clipboard_header = f"""
[SAP CLIPBOARD EXPORT - {datetime.now().strftime('%Y%m%d_%H%M%S')}]
[Source: SAP GUI Transaction Export]
[Format: Plain Text]

"""

        return clipboard_header + clipboard_text
