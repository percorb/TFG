import socket
import threading
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import serial
from sklearn.ensemble import RandomForestClassifier

from FuncionesLector import PrepararDatos, PrepararFila_v3

stop_event_T = None

# Preparación de los datos
def PrepararDataset(ruta):
    global stop_event_T
    stop_event_T = threading.Event()
    csv = pd.read_csv(ruta)
    X = csv.drop(columns=["Label"]).values # Nos da todos los valores menos las etiquetas
    y = csv["Label"].values # Etiquetas, objetivos de la predicción 
    return X,y

def EscalarDatos(X):
    print("Bien aqui 3")
    scaler = StandardScaler()
    print("Bien aqui 4")
    X = scaler.fit_transform(X)
    print("Bien aqui 5")
    return scaler,X

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

def ConectarArduinoLocal():
    arduino = serial.Serial('COM6', 115200) 
    
    return arduino

def ConectarArduinoWifi(ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,5000))
    print("Conectado")
    
    arduino = sock.makefile()
    return arduino

cancel_wifi = threading.Event() # Por si se pulsa otro botón, se cancela la conexión

def ConectarArduinoWifiThread(ip, callback_ok, callback_fail):
    def worker():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            conectado=False
            intentos=0
            while not cancel_wifi.is_set() and intentos<100:
                intentos+=1
                print(f"{intentos}/100")
                try:
                    sock.connect((ip,5000))
                    conectado = True
                    break
                except Exception as e:
                    continue
            
            if not conectado and not cancel_wifi.is_set():
                callback_fail()
                return
            elif not conectado and cancel_wifi.is_set():
                return
                    
            arduino = sock.makefile()
            print("Conectado")
            
            callback_ok(arduino)
            
        except Exception as e:
            print(f"Error durante la conexión WiFi: {e}")
            callback_fail()
    threading.Thread(target=worker,daemon=True).start() # Para que funcione en segundo plano


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
            
def PrediccionRealThread(arduino,ventana,rf, scaler, callback):
    global stop_event_T
    stop_event_T.clear()
    buffer = []
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
                print("Bien")
                caracteristicas,error = PrepararFila_v3(buffer)
                print("Bien 2")
                        
                # Escalamos los datos
                caracteristicas = scaler.transform([caracteristicas])
                print("Bien 3")
                
                # Predicción
                pred = rf.predict(caracteristicas)[0] # Máxima probabilidad
                print("Bien 4")
                
                # Probabilidades
                probs = rf.predict_proba(caracteristicas)[0]
                print("Bien 5")
                
                # Me quedo con las 3 mejores para comprobar
                indices = np.argsort(probs)[::-1][:3]
                print("Bien 6")
                
                top3 = [(rf.classes_[i], probs[i]) for i in indices]
                print("Bien 7")
                
                callback(pred,top3)
                print("Bien 8")
                
                # Vaciamos el buffer y volvemos a leer
                buffer = []
            
        except Exception as e:
            print(f"Error durante la predicción: {e}")
            
def PararTraduccion():
    global stop_event_T
    stop_event_T.set()