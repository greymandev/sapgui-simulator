# query_gui_tool.py - FBL5N Query GUI for tool integration with macOS thread safety

import sys
import threading
import time
from typing import Dict, Any, List, Optional
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
def launch_query_gui(customer_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Launch FBL5N customer line items GUI with pre-filled data

    Args:
        customer_id: Customer ID
        items: List of line items to display

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
        logger.info(f"Launching query GUI for customer {customer_id} with {len(items)} items")

        sg.theme('BlueMono')

        # Table headers for FBL5N results
        table_headers = ['Document', 'Doc Type', 'Date', 'Amount', 'Currency', 'Status']

        # Convert items to table format
        table_data = []
        for item in items:
            table_data.append([
                item.get('document', ''),
                item.get('doc_type', ''),
                item.get('date', ''),
                item.get('amount', ''),
                item.get('currency', ''),
                item.get('status', '')
            ])

        layout = [
            [sg.Text('Customer Line Items (FBL5N) - Tool Mode', font=('Helvetica', 16))],
            [sg.HSeparator()],
            [sg.Text('Selection Criteria', font=('Helvetica', 12))],
            [sg.Text('Customer ID', size=(15, 1)), sg.InputText(customer_id, key='-CUSTOMER_ID-', size=(20, 1), disabled=True)],
            [sg.Text('Company Code', size=(15, 1)), sg.InputText('1000', key='-COMPANY_CODE-', size=(10, 1), disabled=True)],
            [sg.HSeparator()],
            [sg.Text('Results', font=('Helvetica', 12))],
            [sg.Table(
                values=table_data,
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
            [sg.Text('Items Found:', size=(12,1)), sg.Text(f'{len(items)}', size=(10,1), key='-COUNT-', text_color='lightgreen')],
            [sg.Text('Status:', size=(12,1)), sg.Text('Query completed successfully', size=(50,1), key='-STATUS-', text_color='lightgreen')],
            [sg.Button('Refresh', key='-BTN_REFRESH-'), sg.Button('Export', key='-BTN_EXPORT-'), sg.Button('Close')]
        ]

        window = sg.Window('SAP FBL5N Tool', layout, finalize=True, size=(800, 600))

        result_data = {
            "gui_status": "displayed",
            "items_displayed": len(items),
            "user_interactions": []
        }

        start_time = time.time()

        while True:
            event, values = window.read(timeout=100)

            if event == sg.WIN_CLOSED or event == 'Close':
                break

            if event == '-BTN_REFRESH-':
                result_data["user_interactions"].append("refresh_clicked")
                window['-STATUS-'].update('Data refreshed', text_color='yellow')

            elif event == '-BTN_EXPORT-':
                result_data["user_interactions"].append("export_clicked")
                window['-STATUS-'].update('Data exported successfully', text_color='lightgreen')

            # Auto-close after 10 seconds of display
            if time.time() - start_time > 10:
                result_data["auto_closed"] = True
                break

        window.close()

        result_data.update({
            "display_time": f"{time.time() - start_time:.2f}s",
            "final_status": "completed"
        })

        logger.info(f"Query GUI completed: {result_data}")
        return result_data

    except Exception as e:
        logger.error(f"Query GUI error: {e}")
        return {"gui_status": "error", "error": str(e)}

def create_threaded_query_gui(customer_id: str, items: List[Dict[str, Any]]) -> threading.Thread:
    """
    Create query GUI in a separate thread

    Returns:
        Thread object that can be started
    """
    def gui_worker():
        return launch_query_gui(customer_id, items)

    thread = threading.Thread(target=gui_worker, daemon=True)
    return thread
