# test_tools_headless.py - Test tools without GUI

import asyncio
import json
from sap_tools import fbl5n, cobros

async def test_headless_tools():
    """Test SAP tools without GUI (headless mode)"""

    print("🧪 Testing SAP Tools - Headless Mode")
    print("=" * 50)

    # Test 1: Query customer items (no GUI)
    print("\n📊 Test 1: FBL5N Customer Query (headless)")
    try:
        result1 = await fbl5n("123456", with_gui=False)
        print(f"✅ Status: {result1['status']}")
        print(f"✅ Message: {result1['message']}")
        print(f"✅ Items: {result1.get('items_count', 0)}")
        print(f"✅ Time: {result1.get('execution_time')}")
        if result1.get('items'):
            print(f"✅ Sample item: {result1['items'][0]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 2: Process payment (no GUI)
    print("\n💳 Test 2: F-28 Payment Processing (headless)")
    try:
        result2 = await cobros("123456", "1800000789", "1250.75", with_gui=False)
        print(f"✅ Status: {result2['status']}")
        print(f"✅ Message: {result2['message']}")
        print(f"✅ Payment doc: {result2.get('payment_document')}")
        print(f"✅ Time: {result2.get('execution_time')}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Test 3: Error handling
    print("\n❌ Test 3: Error Handling")
    try:
        result3 = await fbl5n("INVALID", with_gui=False)
        print(f"✅ Error handled correctly: {result3['status']}")
        print(f"✅ Error message: {result3['message']}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    print("\n🎉 Headless testing completed!")

if __name__ == "__main__":
    asyncio.run(test_headless_tools())
