# agente_procesador_cobros.py

import FreeSimpleGUI as sg
from fake_sap_scripting_api import MockApplication, MockConnection
import threading
import time

# agente_procesador_cobros.py

import FreeSimpleGUI as sg
from fake_sap_scripting_api import MockApplication, MockConnection
import threading
import time

def run_agent_logic(window):
    """
    Función que ejecuta la lógica del agente una vez que la GUI está lista
    """
    try:
        # El agente simula la conexión a SAP
        SapGui = MockApplication()
        engine = SapGui.GetScriptingEngine()
        
        # En lugar de una conexión real, pasamos nuestra ventana simulada
        connection = MockConnection(window) 
        session = connection.children(0)
        
        print("✅ Agente conectado a la sesión de SAP simulada.")

        # Datos de la transacción a procesar
        cliente_id = "123456"
        documento_a_cancelar = "1800000789"
        importe_cancelado = "1250.75"

        print(f"📄 Procesando cobro para cliente {cliente_id}, doc: {documento_a_cancelar} por {importe_cancelado} EUR.")
        
        # El agente interactúa usando los mismos comandos de SAP Scripting
        session.findById("-CLIENTE-").text = cliente_id
        session.findById("-DOC_NUM-").text = documento_a_cancelar
        session.findById("-IMPORTE-").text = importe_cancelado
        
        time.sleep(2) # Pausa para ver los datos en la GUI
        
        print("🚀 Enviando transacción para contabilizar...")
        session.findById("-BTN_PROCESAR-").press()
        
        time.sleep(1) # Esperar a que la GUI actualice el estado
        
        # El agente recupera el informe de estado final
        status = session.get_status_message()
        print(f"📢 Informe de estado final: '{status}'")

        if "Éxito" in status:
            print("🎉 Transacción completada con éxito.")
        else:
            print("❌ La transacción falló. Revisar el estado.")

    except Exception as e:
        print(f"🔥 Error crítico en el agente: {e}")

# --- SCRIPT PRINCIPAL ---

print("🤖 Iniciando Agente de Procesamiento de Cobros...")

# Crear la GUI en el hilo principal
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

window = sg.Window('Simulador SAP F-28 (Controlado por Agente)', layout, finalize=True)

# Ejecutar la lógica del agente en un hilo separado después de crear la ventana
agent_thread = threading.Thread(target=run_agent_logic, args=(window,), daemon=True)
agent_thread.start()

# Bucle principal de la GUI
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Salir':
        break

window.close()
print("🛑 Simulación finalizada.")