# fake_sap_scripting_api.py

class MockElement:
    """
    Class that mimics a SAP GUI element (e.g., a text field, a button).
    Controls a specific element of the FreeSimpleGUI window.
    """
    def __init__(self, window, key):
        self._window = window
        self._key = key

    @property
    def text(self):
        # Returns the value of the element in the FreeSimpleGUI window.
        return self._window[self._key].get()

    @text.setter
    def text(self, value):
        # Updates the value of the element in the FreeSimpleGUI window.
        self._window[self._key].update(value)

    def press(self):
        # Simulates clicking a button by sending an event
        if self._key == "-BTN_PROCESS-":
            # Simulate payment processing
            self._window['-STATUS-'].update("Processing payment...")
            self._window.refresh()
            import time
            time.sleep(1)
            self._window['-STATUS-'].update("Success: Payment processed successfully")
            self._window.refresh()

class MockSession:
    """Class that mimics the SAP 'session' object."""
    def __init__(self, window):
        self._window = window

    def findById(self, element_id):
        """
        Finds an element by its ID. In our simulation, the ID will be the 'key'
        of FreeSimpleGUI that we defined in the layout.
        
        Example: session.findById("-CUSTOMER-")
        """
        return MockElement(self._window, element_id)

    def get_status_message(self):
        """Gets the message from the simulated status bar."""
        return self._window['-STATUS-'].get()

class MockConnection:
    """Class that mimics the SAP 'connection' object."""
    def __init__(self, window):
        self._window = window

    def children(self, index):
        # In real SAP, children(0) returns the first session.
        # Here, we always return our single simulated session.
        if index == 0:
            return MockSession(self._window)
        return None

class MockApplication:
    """Class that mimics the SAP 'SapGui' object for SAP Scripting."""
    def GetScriptingEngine(self):
        # Returns a fake engine that can "connect".
        return self
        
    def OpenConnection(self, connection_string, WithTicket=None):
         # In a real implementation, this would open a new connection.
         # Here we simply return a MockConnection object to maintain API compatibility.
         # Not strictly necessary for this example, but good to have.
        print(f"Simulating connection to '{connection_string}'...")
        # The real window is passed in the MockConnection constructor
        # in the agent script.
        return True # Simulates that the connection was established successfully