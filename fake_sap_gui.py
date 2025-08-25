# fake_sap_gui.py

import FreeSimpleGUI as sg
import random

def create_f28_gui():
    """Creates and manages the window that simulates the F-28 transaction."""
    
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

    window = sg.Window('SAP F-28 Simulator', layout, finalize=True)

    # Window event loop
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        # Simulated business logic when button is pressed
        if event == '-BTN_PROCESS-':
            customer = values['-CUSTOMER-']
            doc_num = values['-DOC_NUM-']
            amount = values['-AMOUNT-']

            # Simple validations
            if not all([customer, doc_num, amount]):
                window['-STATUS-'].update('Error: Missing mandatory data for payment.', text_color='red')
            elif not customer.isdigit() or len(customer) != 6:
                window['-STATUS-'].update(f'Error: Customer ID "{customer}" is not valid.', text_color='red')
            elif not doc_num.isdigit():
                 window['-STATUS-'].update(f'Error: Document "{doc_num}" is not numeric.', text_color='red')
            else:
                # Success simulation
                payment_doc = random.randint(1400000000, 1499999999)
                message = f'Success: Document {payment_doc} posted in company code 1000.'
                window['-STATUS-'].update(message, text_color='lightgreen')
                
                # Clear fields for next operation
                window['-CUSTOMER-'].update('')
                window['-DOC_NUM-'].update('')
                window['-AMOUNT-'].update('')


    window.close()
    return window

if __name__ == '__main__':
    create_f28_gui()