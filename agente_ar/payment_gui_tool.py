# payment_gui_tool.py - F-28 Payment GUI for tool integration with macOS thread safety

import sys
import threading
import time
from typing import Dict, Any, Optional
import logging

# Import GUI manager for thread safety
try:
    sys.path.append('..')
    from macos_gui_manager import gui_thread_safe, is_gui_safe
except ImportError:
    def gui_thread_safe(func):
        return func
    def is_gui_safe():
        return True

try:
    import FreeSimpleGUI as sg
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

logger = logging.getLogger(__name__)

@gui_thread_safe
def launch_payment_gui(customer: str, doc_num: str, amount: str) -> Dict[str, Any]:
    """
    Launch F-28 payment processing GUI with pre-filled data

    Args:
        customer: Customer ID
        doc_num: Document number
        amount: Payment amount

    Returns:
        Dict with GUI execution results
    """
    if not GUI_AVAILABLE:
        return {
            "gui_launched": False,
            "error": "FreeSimpleGUI not available",
            "recommendation": "Install FreeSimpleGUI or use headless mode"
        }

    if not is_gui_safe():
        return {
            "gui_launched": False,
            "error": "GUI not safe on current thread",
            "recommendation": "Use headless mode or ensure main thread execution"
        }

    try:
        logger.info(f"Launching payment GUI for customer {customer}")

        sg.theme('BlueMono')

        layout = [
            [sg.Text('Payment Processing (F-28) - Tool Mode', font=('Helvetica', 16))],
            [sg.HSeparator()],
            [sg.Text('Header data', font=('Helvetica', 12))],
            [sg.Text('Document date', size=(15, 1)), sg.InputText('25.08.2025', key='-DATE-')],
            [sg.Text('Company code', size=(15, 1)), sg.InputText('1000', key='-COMPANY-')],
            [sg.HSeparator()],
            [sg.Text('Bank data', font=('Helvetica', 12))],
            [sg.Text('Amount', size=(15, 1)), sg.InputText(amount, key='-AMOUNT-')],
            [sg.HSeparator()],
            [sg.Text('Open item selection', font=('Helvetica', 12))],
            [sg.Text('Customer (Bill-to)', size=(15, 1)), sg.InputText(customer, key='-CUSTOMER-')],
            [sg.Text('Document number', size=(15, 1)), sg.InputText(doc_num, key='-DOC_NUM-')],
            [sg.Button('Process Payment', key='-BTN_PROCESS-'), sg.Button('Close')],
            [sg.HSeparator()],
            [sg.Text('Status:', size=(10,1)), sg.Text('Ready for processing...', size=(60,1), key='-STATUS-', text_color='yellow')]
        ]

        window = sg.Window('SAP F-28 Tool', layout, finalize=True, size=(600, 400))

        # Auto-trigger processing after a brief delay
        processing_done = False
        result_data = {}

        start_time = time.time()

        while True:
            event, values = window.read(timeout=100)

            if event == sg.WIN_CLOSED or event == 'Close':
                break

            # Auto-process after 2 seconds or manual trigger
            if (time.time() - start_time > 2 and not processing_done) or event == '-BTN_PROCESS-':
                if not processing_done:
                    window['-STATUS-'].update('Processing payment...', text_color='orange')
                    window.refresh()
                    time.sleep(1)

                    # Simulate successful processing
                    import random
                    doc_number = random.randint(1400000000, 1499999999)
                    window['-STATUS-'].update(f'Success: Document {doc_number} posted in company 1000', text_color='lightgreen')

                    result_data = {
                        "gui_status": "completed",
                        "user_interaction": event == '-BTN_PROCESS-',
                        "processing_time": f"{time.time() - start_time:.2f}s",
                        "document_generated": str(doc_number),
                        "final_values": dict(values)
                    }
                    processing_done = True

            # Auto-close after showing result for 3 seconds
            if processing_done and time.time() - start_time > 5:
                break

        window.close()

        if not result_data:
            result_data = {
                "gui_status": "closed_early",
                "user_interaction": False,
                "processing_time": f"{time.time() - start_time:.2f}s"
            }

        logger.info(f"Payment GUI completed: {result_data}")
        return result_data

    except Exception as e:
        logger.error(f"Payment GUI error: {e}")
        return {"gui_status": "error", "error": str(e)}

def create_threaded_payment_gui(customer: str, doc_num: str, amount: str) -> threading.Thread:
    """
    Create payment GUI in a separate thread

    Returns:
        Thread object that can be started
    """
    def gui_worker():
        return launch_payment_gui(customer, doc_num, amount)

    thread = threading.Thread(target=gui_worker, daemon=True)
    return thread
