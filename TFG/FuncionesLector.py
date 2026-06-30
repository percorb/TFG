import numpy as np

def PrepararDatos(datos):
   
    # Hay que prepararlos uno a uno
    # Los sensores de flexión serán números enteros
    for i in range(0,5):
        datos[i] = int(datos[i])
        
    # Los sensores del giroscopio serán float
    for i in range(5,len(datos)):
        datos[i] = float(datos[i])
    
    return datos

def CalcularPitch(Ax,Ay,Az):
    valor = np.sqrt((np.square(Ay)) + (np.square(Az)))
    return np.arctan2(Ax, valor)

def CalcularRoll(Ay,Az):
    return np.arctan2(Ay, Az)

def PrepararFila_v3(datos):
    datos = np.array(datos)

    # ===== VALIDACIÓN DE ERROR EN DATOS CRUDOS =====
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