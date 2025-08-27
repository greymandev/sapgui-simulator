# langgraph_example.py - Example usage with LangGraph

import asyncio
import json
from typing import Dict, Any
import logging

from sap_tools import fbl5n, cobros

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def example_langgraph_agent():
    """
    Example of how LangGraph agent would use SAP tools
    """

    print("🤖 Starting LangGraph SAP Agent Example...")

    # Simulate agent state
    agent_state = {
        "session_id": "session_123",
        "user_id": "agent_user",
        "conversation_turn": 1
    }

    try:
        # Example 1: Query customer line items
        print("\n📊 Example 1: Querying customer line items (FBL5N)")
        print("=" * 50)

        customer_id = "123456"
        result1 = await fbl5n(customer_id, with_gui=True, state=agent_state)

        print(f"✅ FBL5N Result:")
        print(f"   Status: {result1['status']}")
        print(f"   Message: {result1['message']}")
        print(f"   Items found: {result1.get('items_count', 0)}")
        print(f"   GUI launched: {result1.get('gui_launched', False)}")
        print(f"   Execution time: {result1.get('execution_time', 'N/A')}")

        if result1['status'] == 'success' and result1.get('items'):
            print(f"   Sample items:")
            for i, item in enumerate(result1['items'][:2]):  # Show first 2 items
                print(f"     {i+1}. Doc: {item['document']}, Amount: {item['amount']} {item['currency']}")

        # Wait a bit for GUI to display
        await asyncio.sleep(3)

        # Example 2: Process payment
        print("\n💳 Example 2: Processing payment (F-28)")
        print("=" * 50)

        customer = "123456"
        doc_num = "1800000789"
        amount = "1250.75"

        agent_state["conversation_turn"] = 2
        result2 = await cobros(customer, doc_num, amount, with_gui=True, state=agent_state)

        print(f"✅ F-28 Payment Result:")
        print(f"   Status: {result2['status']}")
        print(f"   Message: {result2['message']}")
        print(f"   Payment document: {result2.get('payment_document', 'N/A')}")
        print(f"   GUI launched: {result2.get('gui_launched', False)}")
        print(f"   Execution time: {result2.get('execution_time', 'N/A')}")

        # Wait for GUI to complete
        await asyncio.sleep(6)

        # Example 3: Error handling
        print("\n❌ Example 3: Error handling")
        print("=" * 50)

        # Invalid customer ID
        result3 = await fbl5n("INVALID", with_gui=False, state=agent_state)

        print(f"❌ Error Result:")
        print(f"   Status: {result3['status']}")
        print(f"   Message: {result3['message']}")
        print(f"   Error: {result3.get('error', 'N/A')}")

        print("\n🎉 LangGraph SAP Agent Example completed!")

        # Return final summary for agent
        return {
            "examples_completed": 3,
            "successful_operations": sum(1 for r in [result1, result2] if r['status'] == 'success'),
            "errors_handled": sum(1 for r in [result3] if r['status'] == 'error'),
            "total_execution_time": f"{sum(float(r.get('execution_time', '0s').replace('s', '')) for r in [result1, result2, result3]):.2f}s"
        }

    except Exception as e:
        logger.error(f"Agent example failed: {e}")
        return {"status": "error", "error": str(e)}

def sync_example():
    """Synchronous wrapper for testing"""
    return asyncio.run(example_langgraph_agent())

if __name__ == "__main__":
    # Run the example
    result = sync_example()
    print(f"\n📋 Final Summary: {json.dumps(result, indent=2)}")
