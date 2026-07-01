# ====================================================================== #
# FuncionesRF.py                                                         #
# Módulo encargado de gestionar la lógica del modelo de machine learning #
# Autor: David Periñán Corbacho                                          #
# ====================================================================== #

import threading
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from FuncionesLector import PrepararDatos, PrepararFila_v3

stop_event_T = None

error = False

# Devuelve si ha habido un error en la traducción de datos
def getErrorTraduccion():
    global error
    return error

# Establece el flag error a False
def setErrorTraduccion():
    global error
    error = False

# Preparación de los datos
def PrepararDataset(ruta):
    global stop_event_T
    stop_event_T = threading.Event()
    csv = pd.read_csv(ruta)
    X = csv.drop(columns=["Label"]).values # Nos da todos los valores menos las etiquetas
    y = csv["Label"].values # Etiquetas, objetivos de la predicción 
    return X,y

# Escala los datos mediante StandardScaler y devuelve el scaler y los datos escalados
def EscalarDatos(X):
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return scaler,X

# Entrena el modelo de Random Forest y devuelve el modelo entrenado
def PrepararModelo(X,y):
    # Preparación del modelo
    rf = RandomForestClassifier(
        n_estimators=1000, # Número de árboles
        random_state=42, # Semilla para poder reproducir resultados
        n_jobs=-1 # Estamos diciendo que las operaciones se puedan hacer en paralelo
    )

    # Entrenamiento del modelo
    rf.fit(X,y)
    
    return rf

# Predicción en tiempo real, bloqueante, no recomendable para usar en la UI
def PrediccionReal(arduino,ventana,rf, scaler):
    buffer = []
    while True:
        try:
            # Leer del arduino
            linea = arduino.readline().decode().strip()
            data = linea.split(',')
            
            if len(data) != 11:
                continue # Vuelve a intentar leer la información hasta tener todas las características
            
            buffer.append(PrepararDatos(data)) # Almacenamos la información en un buffer
            
            if len(buffer) == ventana:
                # Extraemos las características
                caracteristicas,error = PrepararFila_v3(buffer)
                    
                # Escalamos los datos
                caracteristicas = scaler.transform([caracteristicas])
                
                # Predicción
                pred = rf.predict(caracteristicas)[0] # Máxima probabilidad
                
                # Probabilidades
                probs = rf.predict_proba(caracteristicas)[0]
                
                # Me quedo con las 3 mejores para comprobar
                indices = np.argsort(probs)[::-1][:3]
                
                print(f"Predicción: {pred} |" + "|".join(
                    f"{rf.classes_[i]}: {probs[i]:.1%}"
                    for i in indices
                ))
                
                # Vaciamos el buffer y volvemos a leer
                buffer = []
            
        except Exception as e:
            print(f"Error durante la predicción: {e}")

# Predicción en tiempo real, no bloqueante, se utiliza actualmente           
def PrediccionRealThread(arduino,ventana,rf, scaler, callback):
    global stop_event_T, error
    stop_event_T.clear()
    buffer = []
    historial_pred = []
    while not stop_event_T.is_set():
        try:
            # Leer del arduino
            linea = arduino.readline().decode().strip()
            data = linea.split(',')
            
            if len(data) != 11:
                continue # Vuelve a intentar leer la información hasta tener todas las características
            
            buffer.append(PrepararDatos(data)) # Almacenamos la información en un buffer
            
            if len(buffer) == ventana:
                # Extraemos las características
                caracteristicas,error = PrepararFila_v3(buffer)
                if error:
                    arduino.close()
                    return
                # Escalamos los datos
                caracteristicas = scaler.transform([caracteristicas])
                
                # Predicción
                pred_raw = rf.predict(caracteristicas)[0]

                historial_pred.append(pred_raw)

                if len(historial_pred) > 7:
                    historial_pred.pop(0)

                pred = max(set(historial_pred), key=historial_pred.count)
                
                # Probabilidades
                probs = rf.predict_proba(caracteristicas)[0]
                
                # Me quedo con las 3 mejores para comprobar
                indices = np.argsort(probs)[::-1][:3]
                
                top3 = [(rf.classes_[i], probs[i]) for i in indices]
                
                callback(pred,top3)
                
                # Vaciamos el buffer y volvemos a leer
                buffer.clear()
            
        except Exception as e:
            print(f"Error durante la predicción: {e}")

# Para el proceso de traducción a través de un evento    
def PararTraduccion():
    global stop_event_T
    if stop_event_T is not None:
        stop_event_T.set()