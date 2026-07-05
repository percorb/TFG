from unittest.mock import patch
import pandas as pd
import numpy as np

import FuncionesRF

def test_import_FuncionesRF():
    assert FuncionesRF is not None, "El módulo FuncionesRF no se pudo importar correctamente."
    
def test_get_set_Error():
    FuncionesRF.error = True
    
    assert FuncionesRF.getErrorTraduccion(), "El valor de error debería ser True después de establecerlo."

    FuncionesRF.setErrorTraduccion() # Pone a Falso la variable error
    assert not FuncionesRF.getErrorTraduccion(), "El valor de error debería ser False después de llamar a setErrorTraduccion()."

@patch("FuncionesRF.pd.read_csv")
def test_PrepararDataset(mock_read):
    
    mock_read.return_value = pd.DataFrame({
        "A":[1,2],
        "B":[3,4],
        "Label":["Hola","Adios"]
    })

    X, y = FuncionesRF.PrepararDataset("dataset.csv")
    assert X.shape == (2,2)
    assert list(y) == ["Hola","Adios"]

def test_EscalarDatos():
    X = np.array([[1, 2], [3, 4]])

    scaler, datos = FuncionesRF.EscalarDatos(X)

    assert datos.shape == (2, 2)
    assert isinstance(scaler, FuncionesRF.StandardScaler), "El objeto scaler debería ser una instancia de StandardScaler."

def test_PrepararModelo():
    X = np.array([[1, 2], [3, 4]])
    y = np.array(["Hola", "Adios"])

    modelo = FuncionesRF.PrepararModelo(X, y)

    assert isinstance(modelo, FuncionesRF.RandomForestClassifier), "El modelo debería ser una instancia de RandomForestClassifier."

def test_PararTraduccion():
    FuncionesRF.stop_event_T = FuncionesRF.threading.Event()
    FuncionesRF.PararTraduccion() # Paramos la función, ahora el stop_event debe estar en SET
    assert FuncionesRF.stop_event_T.is_set(), "El evento stop_event_T debería estar en SET"


