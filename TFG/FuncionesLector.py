# ======================================================== #
# FUncionesLector.py                                       #
# Módulo encargado de procesar los datos del lector        #
# Autor: David Periñán Corbacho                            #
# ======================================================== #

import numpy as np

# Pasa los datos de string a valores numéricos.
def PrepararDatos(datos):
   
    # Hay que prepararlos uno a uno
    # Los sensores de flexión serán números enteros
    for i in range(0,5):
        datos[i] = int(datos[i])
        
    # Los sensores del giroscopio serán float
    for i in range(5,len(datos)):
        datos[i] = float(datos[i])
    
    return datos

# Calcula el pitch a partir de los valores del acelerómetro (X, Y, Z).
def CalcularPitch(Ax,Ay,Az):
    valor = np.sqrt((np.square(Ay)) + (np.square(Az)))
    return np.arctan2(Ax, valor)

# Calcula el roll a partir de los valores del acelerómetro (Y, Z).
def CalcularRoll(Ay,Az):
    return np.arctan2(Ay, Az)

# Procesa los datos y los convierte en un vector de características para el modelo de predicción.
def PrepararFila_v3(datos):
    datos = np.array(datos)

    # VALIDACIÓN DE ERROR EN DATOS 
    if datos is None or len(datos) != 10:
        return None, True
    
    flex = datos[:, :5].astype(float)      # dedos
    gyro = datos[:, 8:11].astype(float)    # giroscopio crudo

    error_dedo = np.any(flex == 4095)
    error_gyro = np.all(gyro == 0)
    

    error = error_dedo or error_gyro

    if error:
        return None, True

    Informacion = []

    # 1. Media de flexión
    for i in range(0,5):
        Informacion.append(np.mean(datos[:,i]))
    
    # 2. desviación de flexión (cómo varían los dedos durante el gesto)
    for i in range(0,5):
        Informacion.append(np.std(datos[:,i]))
    
    # 3. Pitch/Roll
    Pitch = []
    Roll = []
    for i in range(10):
        Ax, Ay, Az = datos[i,5], datos[i,6], datos[i,7]
        Pitch.append(CalcularPitch(Ax,Ay,Az))
        Roll.append(CalcularRoll(Ay,Az))
    Informacion.append(np.median(Pitch))
    Informacion.append(np.median(Roll))
    
    # 4. rango de Pitch/Roll (dinámica del gesto)
    Informacion.append(np.max(Pitch) - np.min(Pitch))
    Informacion.append(np.max(Roll) - np.min(Roll))
    
    # 5. Magnitudes vectoriales
    Amag = [np.sqrt(datos[i,5]**2 + datos[i,6]**2 + datos[i,7]**2) for i in range(10)]
    Informacion.append(np.mean(Amag))
    Informacion.append(np.std(Amag))
    
    Gmag = [np.sqrt(datos[i,8]**2 + datos[i,9]**2 + datos[i,10]**2) for i in range(10)]
    Informacion.append(np.mean(Gmag))
    Informacion.append(np.std(Gmag))
    
    return [float(x) for x in Informacion], False