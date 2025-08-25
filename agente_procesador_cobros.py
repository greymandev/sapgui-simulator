# agente_procesador_cobros.py

import FreeSimpleGUI as sg
from fake_sap_scripting_api import MockApplication, MockConnection
import threading
import time

# payment_processing_agent.py

import FreeSimpleGUI as sg
from fake_sap_scripting_api import MockApplication, MockConnection
import threading
import time

def run_agent_logic(window):
    """
    Function that executes the agent logic once the GUI is ready
    """
    try:
        # The agent simulates the connection to SAP
        SapGui = MockApplication()
        engine = SapGui.GetScriptingEngine()
        
        # Instead of a real connection, we pass our simulated window
        connection = MockConnection(window) 
        session = connection.children(0)
        
        print("✅ Agent connected to simulated SAP session.")

        # Transaction data to process
        customer_id = "123456"
        document_to_clear = "1800000789"
        cleared_amount = "1250.75"

        print(f"📄 Processing payment for customer {customer_id}, doc: {document_to_clear} for {cleared_amount} EUR.")
        
        # The agent interacts using the same SAP Scripting commands
        session.findById("-CUSTOMER-").text = customer_id
        session.findById("-DOC_NUM-").text = document_to_clear
        session.findById("-AMOUNT-").text = cleared_amount
        
        time.sleep(2) # Pause to see the data in the GUI
        
        print("🚀 Sending transaction for posting...")
        session.findById("-BTN_PROCESS-").press()
        
        time.sleep(1) # Wait for the GUI to update the status
        
        # The agent retrieves the final status report
        status = session.get_status_message()
        print(f"📢 Final status report: '{status}'")

        if "Success" in status:
            print("🎉 Transaction completed successfully.")
        else:
            print("❌ Transaction failed. Check status.")

    except Exception as e:
        print(f"🔥 Critical error in agent: {e}")

# --- MAIN SCRIPT ---

print("🤖 Starting Payment Processing Agent...")

# Create the GUI in the main thread
sg.theme('BlueMono')
layout = [
    [sg.Text('Payment Simulator (F-28)', font=('Helvetica', 16))],
    [sg.HSeparator()],
    [sg.Text('Header data', font=('Helvetica', 12))],
    [sg.Text('Document date', size=(15, 1)), sg.InputText('25.08.2025', key='-DATE-')],
    [sg.Text('Company code', size=(15, 1)), sg.InputText('1000', key='-COMPANY-')],
    [sg.HSeparator()],
    [sg.Text('Bank data', font=('Helvetica', 12))],
    [sg.Text('Amount', size=(15, 1)), sg.InputText(key='-AMOUNT-')],
    [sg.HSeparator()],
    [sg.Text('Open item selection', font=('Helvetica', 12))],
    [sg.Text('Customer (Bill-to)', size=(15, 1)), sg.InputText(key='-CUSTOMER-')],
    [sg.Text('Document number', size=(15, 1)), sg.InputText(key='-DOC_NUM-')],
    [sg.Button('Process Payment', key='-BTN_PROCESS-'), sg.Button('Exit')],
    [sg.HSeparator()],
    [sg.Text('Status:', size=(10,1)), sg.Text('', size=(60,1), key='-STATUS-', text_color='yellow')]
]

window = sg.Window('SAP F-28 Simulator (Agent Controlled)', layout, finalize=True)

# Execute the agent logic in a separate thread after creating the window
agent_thread = threading.Thread(target=run_agent_logic, args=(window,), daemon=True)
agent_thread.start()

# Main GUI loop
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()
print("🛑 Simulation finished.")