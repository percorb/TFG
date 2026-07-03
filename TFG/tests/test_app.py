# Script de test para el módulo app.py
import app
from unittest.mock import MagicMock

def test_import_app():
    assert app is not None, "El módulo app no se pudo importar correctamente."

# Función guardar letra
# - Vacío
def test_guardar_letra_Vacio():
    # Creamos objetos falsos para simular los elementos que usa la función (varios elementos son globales do de la UI)
    app.entry_texto = MagicMock() # Objeto falso
    app.entry_texto.get.return_value = ""
    app.info = MagicMock() # Label falsa
    app.setLetra = MagicMock() # Función falsa
    
    app.GuardarLetra() # Llamamos a la función que queremos probar
    
    assert not app.Letra, "La letra guardada debería estar vacía cuando la entrada es vacía."
    app.setLetra.assert_not_called()
    # Si da fallo, saltará una excepción
    app.info.configure.assert_called_once_with(text="No hay letra seleccionada")

# - Texto
def test_guardar_letra_Texto():
    # Creamos objetos falsos para simular los elementos que usa la función (varios elementos son globales do de la UI)
    app.entry_texto = MagicMock() # Objeto falso
    app.entry_texto.get.return_value = "A"
    app.info = MagicMock() # Label falsa
    app.setLetra = MagicMock() # Función falsa
    
    app.GuardarLetra() # Llamamos a la función que queremos probar
    
    assert app.Letra, "La letra guardada no coincide con la entrada proporcionada."
    app.setLetra.assert_called_once_with("A") is None, "La función setLetra debería ser llamada cuando la entrada no es vacía."
    app.info.configure.assert_called_once_with(text="Letra seleccionada: A")