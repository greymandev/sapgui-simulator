# SAP GUI Simulator

A Python-based SAP GUI simulator that provides automated agents with a realistic SAP interface using the same SAP Scripting API commands used in real SAP systems. Features robust macOS GUI thread safety and LangGraph integration.

## Overview

This project provides a comprehensive mock implementation of the SAP Scripting API, enabling developers to:

- **Test SAP automation scripts** without needing access to a real SAP system
- **Develop and debug SAP agents** in a controlled environment
- **Train AI agents** on SAP workflows using familiar SAP Scripting commands
- **Prototype SAP integrations** quickly and safely
- **Build LangGraph agents** with native SAP tool integration

## ✨ Features

- 🖥️ **GUI Simulation**: Visual interface mimicking SAP transaction screens
- 🤖 **Agent Compatible**: Works with automated agents using SAP Scripting API
- 🔄 **Real API Compatibility**: Uses the same method calls as genuine SAP Scripting
- 📊 **Multiple Transactions**: Simulates common SAP transactions (F-28, FBL5N)
- 🎯 **Easy Testing**: No SAP license or system access required
- 📋 **Data Display**: Interactive tables showing transaction results
- ⚡ **LangGraph Ready**: Async tools for LangGraph agent integration
- 🔧 **Headless Mode**: Core functionality without GUI dependencies
- 🍎 **macOS Thread Safety**: Robust GUI threading for macOS systems
- 📄 **Text Export Simulation**: SAP-like text output for LLM processing
- 🔗 **JSON Conversion**: Automatic text-to-JSON conversion for AI consumption

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- FreeSimpleGUI

### Installation

1. Clone the repository:
```bash
git clone https://github.com/greymandev/sapgui-simulator.git
cd sapgui-simulator
```

2. Install dependencies:
```bash
pip install FreeSimpleGUI
```

### Usage Options

#### **1. LangGraph Agent Integration (Recommended)**

```python
from agente_ar import fbl5n, cobros, text_to_json

# Query customer line items
result = await fbl5n(customer_id="123456", with_gui=False)

# Process payments
result = await cobros(customer="789012", doc_num="1000000001",
                     amount="1500.00", with_gui=False)

# Convert SAP text output to JSON
json_data = await text_to_json(text_data=sap_output,
                               transaction_type="fbl5n")
```

#### **2. Standalone GUI Simulators**
```bash
# F-28 Payment Processing
python fake_sap_gui.py

# FBL5N Customer Line Items
python fbl5n_gui_simulator.py
```

4. **For automated agents:**
```bash
# F-28 payment processing agent
python agente_procesador_cobros.py

# FBL5N customer query agent
python fbl5n_customer_line_items_agent.py
```

5. **For LangGraph integration:**
```bash
cd agente_ar

# Test headless mode (recommended first)
python test_tools_headless.py

# Full example with GUI (macOS: run from main thread)
python langgraph_example.py
```

## Architecture

### Core Components

- **`fake_sap_scripting_api.py`**: Mock implementation of SAP Scripting API classes
- **`agente_procesador_cobros.py`**: Example automated agent for payment processing (F-28)
- **`fbl5n_customer_line_items_agent.py`**: Automated agent for customer line items query (FBL5N)
- **`fake_sap_gui.py`**: Basic F-28 GUI simulator (standalone)
- **`fbl5n_gui_simulator.py`**: Basic FBL5N GUI simulator (standalone)

### API Classes

- `MockApplication`: Simulates `SapGuiAuto.Application`
- `MockConnection`: Simulates SAP connection object
- `MockSession`: Simulates SAP session with `findById()` method
- `MockElement`: Simulates GUI elements (text fields, buttons)

## Usage Example

### F-28 Payment Processing
```python
from fake_sap_scripting_api import MockApplication, MockConnection

# Connect to simulated SAP (same API as real SAP)
SapGui = MockApplication()
engine = SapGui.GetScriptingEngine()
connection = MockConnection(window)  # Pass GUI window
session = connection.children(0)

# Use standard SAP Scripting commands
session.findById("-CUSTOMER-").text = "123456"
session.findById("-DOC_NUM-").text = "1800000789"
session.findById("-AMOUNT-").text = "1250.75"
session.findById("-BTN_PROCESS-").press()

# Get status
status = session.get_status_message()
```

### FBL5N Customer Line Items Query
```python
from fake_sap_scripting_api import MockApplication, MockConnection

# Same connection process
SapGui = MockApplication()
engine = SapGui.GetScriptingEngine()
connection = MockConnection(window)
session = connection.children(0)

# Query customer line items
session.findById("-CUSTOMER_ID-").text = "123456"
session.findById("-COMPANY_CODE-").text = "1000"
session.findById("-BTN_EXECUTE-").press()

# Results are displayed in the table
status = session.get_status_message()
```

## Supported Transactions

Currently implemented:
- **F-28**: Payment Processing (Incoming Payments)
- **FBL5N**: Customer Line Items (Open Items Query)

Planned:
- FB01: Document Entry
- VA01: Sales Order Creation
- MM01: Material Master Creation

## Project Structure

```
sapgui-simulator/
├── README.md
├── .gitignore
├── fake_sap_scripting_api.py           # Core SAP API simulation
├── agente_procesador_cobros.py         # F-28 payment processing agent
├── fbl5n_customer_line_items_agent.py  # FBL5N customer query agent
├── fake_sap_gui.py                     # F-28 standalone GUI
├── fbl5n_gui_simulator.py              # FBL5N standalone GUI
└── agente_ar/                          # 🆕 LangGraph integration module
    ├── sap_core.py                     # Core business logic
    ├── sap_tools.py                    # Async LangGraph tools
    ├── payment_gui_tool.py             # F-28 GUI tool (thread-safe)
    ├── query_gui_tool.py               # FBL5N GUI tool (thread-safe)
    ├── langgraph_example.py            # Usage examples
    ├── test_tools_headless.py          # Headless testing
    └── README.md                       # LangGraph module docs
```

## 🍎 macOS GUI Thread Safety

This simulator includes robust macOS thread safety features to prevent common `NSWindow` threading errors:

### Auto-Detection

The system automatically detects thread safety and switches to appropriate mode:

```python
# Automatically detects if GUI is safe
result = await fbl5n(customer_id="123456", with_gui=True)

# On unsafe threads, automatically switches to headless mode
# Logs: "🚨 GUI requested but not safe on current thread. Switching to headless mode."
```

### Manual Control

```python
# Force headless mode for maximum reliability
result = await fbl5n(customer_id="123456", with_gui=False)

# Check thread safety manually
from macos_gui_manager import is_gui_safe, get_safe_gui_mode
if is_gui_safe():
    print("✅ GUI safe to launch")
else:
    print("⚠️ Use headless mode")
```

### Testing Thread Safety

```bash
# Test thread safety features
python macos_gui_safety_demo.py
```

### Troubleshooting macOS Issues

**Problem**: `NSWindow should only be instantiated on the main thread!`
**Solution**: The system now auto-detects this and switches to headless mode

**Problem**: GUI appears but crashes when interacting
**Solution**: Use headless mode (`with_gui=False`) for maximum stability

**Recommendation**: For production LangGraph agents on macOS, always use headless mode:
```python
# Production-safe approach
result = await fbl5n(customer_id="123456", with_gui=False)
```

## Development

### Adding New Transactions

1. Extend the GUI layout in the agent file
2. Add corresponding element handlers in `MockElement`
3. Implement business logic in the `press()` method
4. Ensure thread safety with `@gui_thread_safe` decorator

### Testing Agents

The simulator allows you to test SAP automation agents by:
1. Running the simulator
2. Observing agent interactions through the GUI (if thread-safe)
3. Using headless mode for reliable testing
4. Validating transaction results through text exports

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-transaction`)
3. Commit your changes (`git commit -am 'Add new transaction'`)
4. Push to the branch (`git push origin feature/new-transaction`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is a simulation tool for development and testing purposes only. It does not connect to real SAP systems and should not be used in production environments.

## Author

**greymandev**

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
