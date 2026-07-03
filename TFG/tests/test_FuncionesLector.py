import numpy as np
import FuncionesLector

def test_import_FuncionesLector():
    assert FuncionesLector is not None, "El módulo FuncionesLector no se pudo importar correctamente."
    
def test_PrepararDatos():
    datos = [
        "1","2","3","4","5",
        "1.1","2.2","3.3","4.4","5.5","6.6"
    ]
    
    resultado = FuncionesLector.PrepararDatos(datos)
    
    # Los cinco primeros deben ser enteros
    for i in range(5):
        assert isinstance(resultado[i], int), f"El valor en la posición {i} debería ser un entero."
    
    # Los siguientes deben ser flotantes
    for i in range(5, len(resultado)):
        assert isinstance(resultado[i], float), f"El valor en la posición {i} debería ser un flotante."
        
def test_CalcularPitch():
    resultado = FuncionesLector.CalcularPitch(1, 0, 0)
    assert np.isclose(resultado, np.pi/2)
    
def test_CalcularRoll():

    resultado = FuncionesLector.CalcularRoll(1,0)

    assert np.isclose(resultado, np.pi/2)

def test_PrepararFila_v3_ErrorFlex():
    datos = []
    
    for _ in range(10):
        datos.append([
            4095, 100, 100, 100, 100,   # Flexión (primer dedo con error)
            1, 1, 1,                    # Acelerómetro
            1, 1, 1                     # Giroscopio
        ])
    
    resultado,error = FuncionesLector.PrepararFila_v3(datos)
    
    assert error, "Debería detectar un error en los datos de flexión."
    assert resultado is None, "El resultado debería ser None cuando hay un error en los datos."
    
def test_PrepararFila_v3_ErrorMPU():
    datos = []
    
    for _ in range(10):
        datos.append([
            100, 100, 100, 100, 100,   # Flexión 
            0, 0, 0,                    # Acelerómetro (Error)
            0, 0, 0                     # Giroscopio (Error)
        ])
    
    resultado,error = FuncionesLector.PrepararFila_v3(datos)
    
    assert error, "Debería detectar un error en los datos de MPU."
    assert resultado is None, "El resultado debería ser None cuando hay un error en los datos."

def test_PrepararFila_v3_Bien():
    datos = []
    
    for _ in range(10):
        datos.append([
            100, 100, 100, 100, 100,   # Flexión
            1, 1, 1,                    # Acelerómetro
            1, 1, 1                     # Giroscopio
        ])
    
    resultado,error = FuncionesLector.PrepararFila_v3(datos)
    
    assert not error, "No debería detectar un error en los datos de flexión."
    assert resultado is not None, "El resultado no debería ser None cuando no hay errores en los datos."