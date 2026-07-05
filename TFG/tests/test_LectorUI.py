from unittest.mock import MagicMock

import Lector_UI

def test_import_LectorUI():
    assert Lector_UI is not None, "No se ha cargado correctamente el módulo Lector_UI"

def test_getMuestra():
    Lector_UI.muestra_actual = 5
    assert Lector_UI.getMuestra() == 5, "getMuestra() no devuelve el valor correcto"

def test_getFila():
    Lector_UI.ultima_fila = "fila_test"
    assert Lector_UI.getFila() == "fila_test", "getFila() no devuelve el valor correcto"

def test_getFin():
    Lector_UI.finalizado = True
    assert Lector_UI.getFin() == True, "getFin() no devuelve el valor correcto"

def test_getError():
    Lector_UI.error = True
    assert Lector_UI.getError() == True, "getError() no devuelve el valor correcto"

def test_setError():
    Lector_UI.error = True
    Lector_UI.setError()
    assert Lector_UI.error == False, "setError() no establece el valor de error a False"

def test_EscribirFila():
    Lector_UI.file = MagicMock()
    Lector_UI.Letra = "A"

    fila = [1,2,3]
    Lector_UI.EscribirFila(fila)
    Lector_UI.file.write.assert_called_once_with("A,1,2,3\n")

def test_ContinuarLectura():
    Lector_UI.pause_event = Lector_UI.threading.Event()
    Lector_UI.ContinuarLectura()
    assert Lector_UI.pause_event.is_set(), "ContinuarLectura() no establece el evento de pausa correctamente"

def test_PararLectura():
    Lector_UI.pause_event = Lector_UI.threading.Event()
    Lector_UI.stop_event = Lector_UI.threading.Event()
    Lector_UI.PararLectura()
    assert Lector_UI.pause_event.is_set() and Lector_UI.stop_event.is_set(), "PararLectura() no establece el evento de pausa correctamente"
