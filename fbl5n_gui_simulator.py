# fbl5n_gui_simulator.py

import FreeSimpleGUI as sg
import random
from datetime import datetime, timedelta

def create_fbl5n_gui():
    """Creates and manages the window that simulates the FBL5N transaction."""

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

    window = sg.Window('SAP FBL5N Simulator', layout, finalize=True, size=(800, 600))

    # Window event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Simulated business logic when execute button is pressed
        if event == '-BTN_EXECUTE-':
            customer_id = values['-CUSTOMER_ID-']
            company_code = values['-COMPANY_CODE-']

            # Simple validations
            if not customer_id:
                window['-STATUS-'].update('Error: Customer ID is required.', text_color='red')
            elif not customer_id.isdigit() or len(customer_id) != 6:
                window['-STATUS-'].update(f'Error: Customer ID "{customer_id}" is not valid.', text_color='red')
            else:
                # Success simulation - generate sample data
                window['-STATUS-'].update('Executing query...', text_color='yellow')
                window.refresh()

                # Simulate processing time
                import time
                time.sleep(1)

                # Generate random sample data
                sample_data = []
                doc_types = ['Invoice', 'Credit Memo', 'Payment', 'Debit Memo']
                currencies = ['EUR', 'USD', 'GBP']
                statuses = ['Open', 'Partially Paid', 'Overdue']

                num_items = random.randint(3, 8)
                for i in range(num_items):
                    doc_num = f"180000{random.randint(1000, 9999)}"
                    doc_type = random.choice(doc_types)

                    # Random date within last 90 days
                    days_ago = random.randint(1, 90)
                    doc_date = (datetime.now() - timedelta(days=days_ago)).strftime("%d.%m.%Y")

                    # Random amount
                    if doc_type == 'Credit Memo':
                        amount = f"-{random.randint(100, 5000):.2f}"
                    else:
                        amount = f"{random.randint(500, 10000):.2f}"

                    currency = random.choice(currencies)
                    status = random.choice(statuses)

                    sample_data.append([doc_num, doc_type, doc_date, amount, currency, status])

                # Update the table with sample data
                window['-TABLE-'].update(values=sample_data)

                message = f'Success: Found {len(sample_data)} items for customer {customer_id}'
                window['-STATUS-'].update(message, text_color='lightgreen')

        elif event == '-BTN_CLEAR-':
            # Clear the table and input fields
            window['-TABLE-'].update(values=[])
            window['-CUSTOMER_ID-'].update('')
            window['-STATUS-'].update('Ready', text_color='yellow')

    window.close()
    return window

if __name__ == '__main__':
    create_fbl5n_gui()
