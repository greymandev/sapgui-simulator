# Agente AR - LangGraph SAP Tools

This module provides **asynchronous SAP tools** designed for integration with **LangGraph agents**. It includes both core business logic and optional GUI components for enhanced user interaction.

## 🚀 Features

- **🔧 LangGraph Compatible**: Async tools ready for LangGraph integration
- **🖥️ Optional GUI**: Asynchronous GUI support for visual feedback
- **📊 Comprehensive Logging**: Tool execution tracking with timestamps and state context
- **🎯 Error Handling**: Robust error management and reporting
- **⚡ High Performance**: Separate core logic from GUI for optimal performance

## 📁 Module Structure

```
agente_ar/
├── sap_core.py                 # Core SAP business logic (no GUI dependencies)
├── sap_tools.py                # LangGraph async tools with logging
├── payment_gui_tool.py         # F-28 payment processing GUI
├── query_gui_tool.py          # FBL5N customer query GUI
├── langgraph_example.py        # Usage examples and testing
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## 🛠️ Available Tools

### 1. **`fbl5n(customer_id: str)`** - Customer Line Items Query
```python
# Query customer open items (FBL5N transaction)
result = await fbl5n("123456")

# Response format:
{
    "status": "success",
    "message": "Found 5 open items for customer 123456",
    "customer_id": "123456",
    "items_count": 5,
    "items": [
        {
            "document": "1800000789",
            "doc_type": "Invoice",
            "date": "25.08.2025",
            "amount": "1250.75",
            "currency": "EUR",
            "status": "Open"
        }
    ],
    "gui_launched": true,
    "execution_time": "1.23s"
}
```

### 2. **`cobros(customer, doc_num, amount)`** - Payment Processing
```python
# Process payment (F-28 transaction)
result = await cobros("123456", "1800000789", "1250.75")

# Response format:
{
    "status": "success",
    "message": "Payment processed successfully. Document 1400000123 posted in company 1000",
    "payment_document": "1400000123",
    "customer_id": "123456",
    "cleared_document": "1800000789",
    "amount": "1250.75",
    "gui_launched": true,
    "execution_time": "1.45s"
}
```

## 📊 Logging Features

Each tool execution logs:
- ✅ **Tool name** and timestamp
- ✅ **Input arguments**
- ✅ **Output results** summary
- ✅ **Agent state context**
- ✅ **Execution time**
- ✅ **Error details** (if any)

Example log entry:
```json
{
    "tool_name": "fbl5n",
    "timestamp": "2025-08-27T10:30:15.123456",
    "input_args": {"customer_id": "123456", "with_gui": true},
    "output_result": {
        "status": "success",
        "message": "Found 5 open items for customer 123456",
        "data_summary": "5 items"
    },
    "state_context": {"session_id": "session_123", "user_id": "agent_user"},
    "execution_time": "1.23s"
}
```

## 🔧 Quick Start

### 1. Basic Usage
```python
import asyncio
from sap_tools import fbl5n, cobros

async def main():
    # Query customer items
    items_result = await fbl5n("123456")

    # Process payment
    payment_result = await cobros("123456", "1800000789", "1250.75")

    print(f"Items found: {items_result.get('items_count', 0)}")
    print(f"Payment doc: {payment_result.get('payment_document', 'N/A')}")

# Run async function
asyncio.run(main())
```

### 2. With LangGraph Integration
```python
from langgraph import create_agent_executor
from sap_tools import fbl5n, cobros

# Define LangGraph tools
tools = [fbl5n, cobros]

# Create agent with SAP tools
agent = create_agent_executor(
    model=your_llm_model,
    tools=tools,
    # ... other LangGraph configuration
)

# Agent can now call:
# - fbl5n("123456")
# - cobros("123456", "1800000789", "1250.75")
```

### 3. Without GUI (Headless Mode)
```python
# Disable GUI for faster execution
result = await fbl5n("123456", with_gui=False)
result = await cobros("123456", "1800000789", "1250.75", with_gui=False)
```

## 🎯 Tool Parameters

### `fbl5n(customer_id, with_gui=True, state=None)`
- **`customer_id`**: 6-digit customer ID (required)
- **`with_gui`**: Show GUI interface (default: True)
- **`state`**: Agent state context for logging (optional)

### `cobros(customer, doc_num, amount, with_gui=True, state=None)`
- **`customer`**: 6-digit customer ID (required)
- **`doc_num`**: Document number to clear (required)
- **`amount`**: Payment amount (required)
- **`with_gui`**: Show GUI interface (default: True)
- **`state`**: Agent state context for logging (optional)

## 🚨 Error Handling

Tools return consistent error format:
```json
{
    "status": "error",
    "message": "Tool execution failed: Invalid customer ID",
    "error": "Invalid customer ID: INVALID",
    "execution_time": "0.05s",
    "tool_type": "customer_query"
}
```

## 🧪 Testing

Run the example to test all functionality:
```bash
cd agente_ar
python langgraph_example.py
```

This will:
- ✅ Test both tools with valid inputs
- ✅ Launch GUIs for visual verification
- ✅ Test error handling with invalid inputs
- ✅ Show logging output
- ✅ Provide execution summary

## 🔗 Integration with Parent Project

This module is designed to work alongside the original SAP GUI simulator:
- **Original project**: Interactive GUI simulators and standalone agents
- **agente_ar**: LangGraph-compatible async tools with optional GUI

Both can coexist and share the same SAP simulation concepts.

## 📋 Requirements

- Python 3.8+
- FreeSimpleGUI 5.2.0+
- asyncio support
- Optional: LangGraph for full agent integration

## 🆘 Support

For issues or questions regarding LangGraph integration, check the example file and logging output for debugging information.
