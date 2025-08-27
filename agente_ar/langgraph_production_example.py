#!/usr/bin/env python3
"""
LangGraph Example - Headless Mode
=================================

This is a production-ready version of the LangGraph example using headless mode
for maximum reliability on all platforms, especially macOS.
"""

import asyncio
import json
from typing import Dict, Any
import logging

from sap_tools import fbl5n, cobros, text_to_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def production_langgraph_agent():
    """
    Production-ready LangGraph agent example using headless mode
    """

    print("🚀 Production LangGraph SAP Agent Example (Headless Mode)")
    print("=" * 60)

    # Simulate agent state
    agent_state = {
        "session_id": "prod_session_456",
        "user_id": "production_agent",
        "conversation_turn": 1,
        "mode": "headless_production"
    }

    try:
        # Example 1: Query customer line items (headless)
        print("\n📊 Step 1: Querying customer line items (FBL5N)")
        print("-" * 50)

        customer_id = "789012"
        result1 = await fbl5n(customer_id, with_gui=False, state=agent_state)

        print(f"✅ FBL5N Result:")
        print(f"   Status: {result1['status']}")
        print(f"   Message: {result1['message']}")
        print(f"   GUI launched: {result1.get('gui_launched', False)}")
        print(f"   Text export available: {result1.get('text_export', {}).get('export_available', False)}")

        # Get text export for conversion
        sap_text = result1.get('text_export', {}).get('sap_output', '')

        if sap_text:
            print(f"   SAP text generated: {len(sap_text)} characters")

            # Convert to JSON for LLM consumption
            print("\n🔄 Converting SAP text to JSON...")
            json_result = await text_to_json(text_data=sap_text, transaction_type="fbl5n", state=agent_state)

            if 'error' not in json_result:
                print(f"   ✅ JSON conversion successful")
                print(f"   Customer ID: {json_result.get('customer_id', 'N/A')}")
                print(f"   Items found: {len(json_result.get('items', []))}")
                print(f"   Total amount: {json_result.get('summary', {}).get('total_amount', 0)} EUR")
            else:
                print(f"   ❌ JSON conversion failed: {json_result.get('error')}")

        # Example 2: Process payment (headless)
        print("\n💳 Step 2: Processing payment (F-28)")
        print("-" * 50)

        customer = "789012"
        doc_num = "1000000001"
        amount = "2500.00"

        agent_state["conversation_turn"] = 2
        result2 = await cobros(customer, doc_num, amount, with_gui=False, state=agent_state)

        print(f"✅ F-28 Payment Result:")
        print(f"   Status: {result2['status']}")
        print(f"   Message: {result2['message']}")
        print(f"   Payment document: {result2.get('payment_document', 'N/A')}")
        print(f"   GUI launched: {result2.get('gui_launched', False)}")
        print(f"   Text export available: {result2.get('text_export', {}).get('export_available', False)}")

        # Get F-28 text export
        f28_text = result2.get('text_export', {}).get('sap_output', '')

        if f28_text:
            print(f"   SAP text generated: {len(f28_text)} characters")

            # Convert F-28 to JSON
            print("\n🔄 Converting F-28 text to JSON...")
            f28_json_result = await text_to_json(text_data=f28_text, transaction_type="f28", state=agent_state)

            if 'error' not in f28_json_result:
                print(f"   ✅ JSON conversion successful")
                print(f"   Customer ID: {f28_json_result.get('customer_id', 'N/A')}")
                print(f"   Payment amount: {f28_json_result.get('payment_amount', 0)} {f28_json_result.get('currency', 'EUR')}")
                print(f"   Document: {f28_json_result.get('payment_document', 'N/A')}")

        # Example 3: Batch operations
        print("\n📊 Step 3: Batch operations for multiple customers")
        print("-" * 50)

        customers = ["111111", "222222", "333333"]
        batch_results = []

        for i, cust_id in enumerate(customers):
            agent_state["conversation_turn"] = 3 + i
            batch_result = await fbl5n(cust_id, with_gui=False, state=agent_state)
            batch_results.append({
                "customer": cust_id,
                "status": batch_result['status'],
                "items_count": len(batch_result.get('items', [])),
                "execution_time": batch_result.get('execution_time', 'N/A')
            })

        print(f"✅ Batch Processing Results:")
        for result in batch_results:
            print(f"   Customer {result['customer']}: {result['status']} - {result['items_count']} items ({result['execution_time']})")

        print("\n🎉 Production LangGraph Agent Example completed successfully!")

        # Return comprehensive summary
        return {
            "mode": "production_headless",
            "examples_completed": 3,
            "successful_operations": sum(1 for r in [result1, result2] if r['status'] == 'success'),
            "batch_operations": len(batch_results),
            "json_conversions": 2,
            "text_exports_generated": 2,
            "total_customers_processed": len(customers) + 2,
            "agent_state_final": agent_state
        }

    except Exception as e:
        logger.error(f"Production agent example failed: {e}")
        return {"status": "error", "error": str(e), "mode": "production_headless"}

def run_production_example():
    """Run the production example"""
    return asyncio.run(production_langgraph_agent())

if __name__ == "__main__":
    print("🎯 Running Production-Ready LangGraph Example...")
    result = run_production_example()
    print(f"\n📋 Final Production Summary:")
    print(json.dumps(result, indent=2))
