from unittest.mock import MagicMock, patch
import FuncionesArduino

def test_import_FuncionesArduino():
    assert FuncionesArduino is not None, "El módulo FuncionesArduino no se pudo importar correctamente."

@patch('FuncionesArduino.serial.Serial') # Cambia los serial.Serial por un objeto simulado
def test_ConectarArduinoLocal(mock_serial):
    resultado = FuncionesArduino.ConectarArduinoLocal()
    
    # asserts
    mock_serial.assert_called_once_with('COM6', 115200) # Verifica que se haya llamado con los parámetros correctos
    assert resultado == mock_serial.return_value, "La función ConectarArduinoLocal no devuelve el objeto esperado."

@patch('FuncionesArduino.socket.socket') # Cambia los socket.socket por un objeto simulado
def test_ConectarArduinoWifi(mock_socket):
    socket_falso = mock_socket.return_value
    archivo_falso = socket_falso.makefile.return_value
    
    resultado = FuncionesArduino.ConectarArduinoWifi("192.168.1.100")
    
    mock_socket.assert_called_once_with(FuncionesArduino.socket.AF_INET, FuncionesArduino.socket.SOCK_STREAM) # Verifica que se haya llamado con los parámetros correctos
    socket_falso.connect.assert_called_once_with(("192.168.1.100", 5000)) # Verifica que se haya llamado con los parámetros correctos
    assert resultado == archivo_falso, "La función ConectarArduinoWifi no devuelve el objeto esperado."

@patch('FuncionesArduino.threading.Thread') # Cambia los threading.Thread por un objeto simulado
@patch('FuncionesArduino.socket.socket') # Cambia los socket.socket por un objeto simulado
def test_ConectarArduinoWifiThread(mock_socket, mock_thread):
    # Evitamos que se cancele la conexión
    FuncionesArduino.cancel_wifi.clear()
    
    socket_falso = mock_socket.return_value
    socket_falso.makefile.return_value = MagicMock() # Simulamos el archivo devuelto por makefile()

    callback_ok = MagicMock()
    callback_fail = MagicMock()
    # Cuando se vaya a ejecutar el hilo, se ejecuta directamente el worker()
    def ejecutar_worker(target, daemon):
        target()  # Ejecuta la función worker directamente
        return MagicMock()  # Retorna un objeto simulado para el hilo

    mock_thread.side_effect = ejecutar_worker
    
    FuncionesArduino.ConectarArduinoWifiThread("192.168.1.100", callback_ok, callback_fail)
    
    callback_ok.assert_called_once()  # Verifica que se haya llamado al callback de éxito
    callback_fail.assert_not_called()  # Verifica que no se haya llamado al callback de fallo
