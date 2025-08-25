# fake_sap_gui.py

import PySimpleGUI as sg
import random

def create_f28_gui():
    """Crea y gestiona la ventana que simula la transacción F-28."""
    
    sg.theme('BlueMono')

    layout = [
        [sg.Text('Simulador de Cobro (F-28)', font=('Helvetica', 16))],
        [sg.HSeparator()],
        [sg.Text('Datos de cabecera', font=('Helvetica', 12))],
        [sg.Text('Fecha documento', size=(15, 1)), sg.InputText('25.08.2025', key='-FECHA-')],
        [sg.Text('Sociedad', size=(15, 1)), sg.InputText('1000', key='-SOCIEDAD-')],
        [sg.HSeparator()],
        [sg.Text('Datos bancarios', font=('Helvetica', 12))],
        [sg.Text('Importe', size=(15, 1)), sg.InputText(key='-IMPORTE-')],
        [sg.HSeparator()],
        [sg.Text('Selección de partidas abiertas', font=('Helvetica', 12))],
        [sg.Text('Cliente (Bill-to)', size=(15, 1)), sg.InputText(key='-CLIENTE-')],
        [sg.Text('Nº Documento', size=(15, 1)), sg.InputText(key='-DOC_NUM-')],
        [sg.Button('Procesar Cobro', key='-BTN_PROCESAR-'), sg.Button('Salir')],
        [sg.HSeparator()],
        [sg.Text('Estado:', size=(10,1)), sg.Text('', size=(60,1), key='-ESTADO-', text_color='yellow')]
    ]

    window = sg.Window('Simulador SAP F-28', layout, finalize=True)

    # Bucle de eventos de la ventana
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Salir':
            break

        # Lógica de negocio simulada al pulsar el botón
        if event == '-BTN_PROCESAR-':
            cliente = values['-CLIENTE-']
            doc_num = values['-DOC_NUM-']
            importe = values['-IMPORTE-']

            # Validaciones simples
            if not all([cliente, doc_num, importe]):
                window['-ESTADO-'].update('Error: Faltan datos obligatorios para el cobro.', text_color='red')
            elif not cliente.isdigit() or len(cliente) != 6:
                window['-ESTADO-'].update(f'Error: ID de cliente "{cliente}" no es válido.', text_color='red')
            elif not doc_num.isdigit():
                 window['-ESTADO-'].update(f'Error: Documento "{doc_num}" no es numérico.', text_color='red')
            else:
                # Simulación de éxito
                doc_cobro = random.randint(1400000000, 1499999999)
                mensaje = f'Éxito: Documento {doc_cobro} contabilizado en la sociedad 1000.'
                window['-ESTADO-'].update(mensaje, text_color='lightgreen')
                
                # Limpiamos los campos para la siguiente operación
                window['-CLIENTE-'].update('')
                window['-DOC_NUM-'].update('')
                window['-IMPORTE-'].update('')


    window.close()
    return window

if __name__ == '__main__':
    create_f28_gui()