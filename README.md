# SAP GUI Simulator

A Python-based SAP GUI simulator that allows automated agents to interact with a simulated SAP interface using the same SAP Scripting API commands used in real SAP systems.

## Overview

This project provides a mock implementation of the SAP Scripting API, enabling developers to:

- **Test SAP automation scripts** without needing access to a real SAP system
- **Develop and debug SAP agents** in a controlled environment  
- **Train AI agents** on SAP workflows using familiar SAP Scripting commands
- **Prototype SAP integrations** quickly and safely

## Features

- 🖥️ **GUI Simulation**: Visual interface mimicking SAP transaction screens
- 🤖 **Agent Compatible**: Works with automated agents using SAP Scripting API
- 🔄 **Real API Compatibility**: Uses the same method calls as genuine SAP Scripting
- 📊 **Transaction Processing**: Simulates common SAP transactions (F-28 Payment Processing)
- 🎯 **Easy Testing**: No SAP license or system access required

## Quick Start

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

3. Run the payment processing agent:
```bash
python agente_procesador_cobros.py
```

## Architecture

### Core Components

- **`fake_sap_scripting_api.py`**: Mock implementation of SAP Scripting API classes
- **`agente_procesador_cobros.py`**: Example automated agent for payment processing
- **`fake_sap_gui.py`**: Basic GUI simulator (if needed)

### API Classes

- `MockApplication`: Simulates `SapGuiAuto.Application`
- `MockConnection`: Simulates SAP connection object
- `MockSession`: Simulates SAP session with `findById()` method
- `MockElement`: Simulates GUI elements (text fields, buttons)

## Usage Example

```python
from fake_sap_scripting_api import MockApplication, MockConnection

# Connect to simulated SAP (same API as real SAP)
SapGui = MockApplication()
engine = SapGui.GetScriptingEngine()
connection = MockConnection(window)  # Pass GUI window
session = connection.children(0)

# Use standard SAP Scripting commands
session.findById("-CLIENTE-").text = "123456"
session.findById("-DOC_NUM-").text = "1800000789"
session.findById("-IMPORTE-").text = "1250.75"
session.findById("-BTN_PROCESAR-").press()

# Get status
status = session.get_status_message()
```

## Supported Transactions

Currently implemented:
- **F-28**: Payment Processing (Incoming Payments)

Planned:
- FB01: Document Entry
- VA01: Sales Order Creation
- MM01: Material Master Creation

## Project Structure

```
sapgui-simulator/
├── README.md
├── .gitignore
├── fake_sap_scripting_api.py    # Core SAP API simulation
├── agente_procesador_cobros.py  # Payment processing agent
└── fake_sap_gui.py             # Basic GUI (optional)
```

## Development

### Adding New Transactions

1. Extend the GUI layout in the agent file
2. Add corresponding element handlers in `MockElement`
3. Implement business logic in the `press()` method

### Testing Agents

The simulator allows you to test SAP automation agents by:
1. Running the simulator
2. Observing agent interactions through the GUI
3. Validating transaction results

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
