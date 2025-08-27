# fbl5n_customer_line_items_agent.py

import FreeSimpleGUI as sg
from fake_sap_scripting_api import MockApplication, MockConnection
import threading
import time

def run_agent_logic(window):
    """
    Function that executes the FBL5N agent logic once the GUI is ready
    """
    try:
        # The agent simulates the connection to SAP
        SapGui = MockApplication()
        engine = SapGui.GetScriptingEngine()

        # Instead of a real connection, we pass our simulated window
        connection = MockConnection(window)
        session = connection.children(0)

        print("✅ FBL5N Agent connected to simulated SAP session.")

        # Customer data to query
        customer_id = "123456"
        company_code = "1000"

        print(f"📄 Querying open items for customer {customer_id} in company {company_code}.")

        # The agent interacts using the same SAP Scripting commands
        session.findById("-CUSTOMER_ID-").text = customer_id
        session.findById("-COMPANY_CODE-").text = company_code

        # Set date range (last 30 days)
        from datetime import datetime, timedelta
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)

        session.findById("-DATE_FROM-").text = start_date.strftime("%d.%m.%Y")
        session.findById("-DATE_TO-").text = end_date.strftime("%d.%m.%Y")

        time.sleep(2) # Pause to see the data in the GUI

        print("🚀 Executing FBL5N query...")
        session.findById("-BTN_EXECUTE-").press()

        time.sleep(2) # Wait for the GUI to update with results

        # The agent retrieves the final status report
        status = session.get_status_message()
        print(f"📢 Query result: '{status}'")

        if "Success" in status:
            print("🎉 FBL5N query executed successfully.")
            print("📊 Open items displayed in the table.")
        else:
            print("❌ Query failed. Check parameters.")

    except Exception as e:
        print(f"🔥 Critical error in FBL5N agent: {e}")

# --- MAIN SCRIPT ---

print("🤖 Starting FBL5N Customer Line Items Agent...")

# Create the GUI in the main thread
sg.theme('BlueMono')

# Table headers for FBL5N results
table_headers = ['Document', 'Doc Type', 'Date', 'Amount', 'Currency', 'Status']

layout = [
    [sg.Text('Customer Line Items (FBL5N)', font=('Helvetica', 16))],
    [sg.HSeparator()],
    [sg.Text('Selection Criteria', font=('Helvetica', 12))],
    [sg.Text('Customer ID', size=(15, 1)), sg.InputText(key='-CUSTOMER_ID-', size=(20, 1))],
    [sg.Text('Company Code', size=(15, 1)), sg.InputText('1000', key='-COMPANY_CODE-', size=(10, 1))],
    [sg.Text('Date From', size=(15, 1)), sg.InputText(key='-DATE_FROM-', size=(12, 1))],
    [sg.Text('Date To', size=(15, 1)), sg.InputText(key='-DATE_TO-', size=(12, 1))],
    [sg.HSeparator()],
    [sg.Text('Additional Options', font=('Helvetica', 12))],
    [sg.Checkbox('Open Items Only', default=True, key='-OPEN_ONLY-')],
    [sg.Checkbox('All Line Items', default=False, key='-ALL_ITEMS-')],
    [sg.HSeparator()],
    [sg.Button('Execute Query', key='-BTN_EXECUTE-'), sg.Button('Clear', key='-BTN_CLEAR-'), sg.Button('Exit')],
    [sg.HSeparator()],
    [sg.Text('Results', font=('Helvetica', 12))],
    [sg.Table(
        values=[],
        headings=table_headers,
        max_col_width=25,
        auto_size_columns=True,
        display_row_numbers=False,
        justification='left',
        num_rows=10,
        key='-TABLE-',
        row_height=25,
        alternating_row_color='lightblue'
    )],
    [sg.HSeparator()],
    [sg.Text('Status:', size=(10,1)), sg.Text('Ready', size=(60,1), key='-STATUS-', text_color='yellow')]
]

window = sg.Window('SAP FBL5N Simulator (Agent Controlled)', layout, finalize=True, size=(800, 600))

# Execute the agent logic in a separate thread after creating the window
agent_thread = threading.Thread(target=run_agent_logic, args=(window,), daemon=True)
agent_thread.start()

# Main GUI loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == '-BTN_CLEAR-':
        # Clear the table and input fields
        window['-TABLE-'].update(values=[])
        window['-CUSTOMER_ID-'].update('')
        window['-STATUS-'].update('Ready')

window.close()
print("🛑 FBL5N Simulation finished.")
