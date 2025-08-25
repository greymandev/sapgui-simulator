# fake_sap_scripting_api.py

class MockElement:
    """
    Clase que imita un elemento de la GUI de SAP (ej. un campo de texto, un botón).
    Controla un elemento específico de la ventana de PySimpleGUI.
    """
    def __init__(self, window, key):
        self._window = window
        self._key = key

    @property
    def text(self):
        # Devuelve el valor del elemento en la ventana PySimpleGUI.
        return self._window[self._key].get()

    @text.setter
    def text(self, value):
        # Actualiza el valor del elemento en la ventana PySimpleGUI.
        self._window[self._key].update(value)

    def press(self):
        # Simula hacer clic en un botón enviando un evento
        if self._key == "-BTN_PROCESAR-":
            # Simular el procesamiento del cobro
            self._window['-ESTADO-'].update("Procesando cobro...")
            self._window.refresh()
            import time
            time.sleep(1)
            self._window['-ESTADO-'].update("Éxito: Cobro procesado correctamente")
            self._window.refresh()

class MockSession:
    """Clase que imita el objeto 'session' de SAP."""
    def __init__(self, window):
        self._window = window

    def findById(self, element_id):
        """
        Busca un elemento por su ID. En nuestra simulación, el ID será la 'key'
        de PySimpleGUI que definimos en el layout.
        
        Ejemplo: session.findById("-CLIENTE-")
        """
        return MockElement(self._window, element_id)

    def get_status_message(self):
        """Obtiene el mensaje de la barra de estado simulada."""
        return self._window['-ESTADO-'].get()

class MockConnection:
    """Clase que imita el objeto 'connection' de SAP."""
    def __init__(self, window):
        self._window = window

    def children(self, index):
        # En SAP real, children(0) devuelve la primera sesión.
        # Aquí, siempre devolvemos nuestra única sesión simulada.
        if index == 0:
            return MockSession(self._window)
        return None

class MockApplication:
    """Clase que imita el objeto 'SapGui' de SAP Scripting."""
    def GetScriptingEngine(self):
        # Devuelve un motor falso que puede "conectar".
        return self
        
    def OpenConnection(self, connection_string, WithTicket=None):
         # En una implementación real, esto abriría una nueva conexión.
         # Aquí simplemente devolvemos un objeto MockConnection para mantener la compatibilidad de la API.
         # No es estrictamente necesario para este ejemplo, pero es bueno tenerlo.
        print(f"Simulando conexión a '{connection_string}'...")
        # La ventana real se pasa en el constructor de MockConnection
        # en el script del agente.
        return True # Simula que la conexión se estableció correctamente