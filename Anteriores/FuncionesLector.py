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

def PrepararFila(datos):
    # Pasamos la lista de listas a una matriz
    datos = np.array(datos)
    # Ahora tenemos una matriz, en el que cada fila es una muestra.
    Informacion = []
    # de la matriz sacaremos un único vector con toda la información
    # - Sensores de flexión [0-4]
    # Calcularemos la media de las filas de las 5 primeras columnas
    for i in range(0,5):
        media = np.mean(datos[:,i])
        Informacion.append(media)
    
    # Una vez obtenido las medias de los sensores de flexión, pasamos a los sensores del giroscopio
    # De aquí se obtendrán la media, la desviación típica de cada eje y de su magnitud vectorial
    
    # Aceleración
    # - Media y desviacion estándar normal
    for i in range(5,8):
        media = np.mean(datos[:,i])
        desv = np.std(datos[:,i])
        Informacion.append(media)
        Informacion.append(desv)
    
    # - Media y desviación estándar de la magnitud vectorial (sqrt(Ax^2 + Ay^2 + Az^2))
    Amag = []
    for i in range(0,10):
        Amag.append(np.sqrt((np.square(datos[i,5])) + (np.square(datos[i,6])) + (np.square(datos[i,7]))))
    media = np.mean(Amag)
    desv = np.std(Amag)
    Informacion.append(media)
    Informacion.append(desv)
    
    # Giro
    for i in range(8,11):
        media = np.mean(datos[:,i])
        desv = np.std(datos[:,i])
        Informacion.append(media)
        Informacion.append(desv)
    
    # - Media y desviación estándar de la magnitud vectorial (sqrt(Gx^2 + Gy^2 + Gz^2))
    Gmag = []
    for i in range(0,10):
        Gmag.append(np.sqrt((np.square(datos[i,8])) + (np.square(datos[i,9])) + (np.square(datos[i,10]))))
    media = np.mean(Gmag)
    desv = np.std(Gmag)
    Informacion.append(media)
    Informacion.append(desv)
    
    # Pasamos los datos a float
    Informacion = [float(x) for x in Informacion]
    
    return Informacion

def CalcularPitch(Ax,Ay,Az):
    valor = np.sqrt((np.square(Ay)) + (np.square(Az)))
    return np.arctan2(Ax, valor)

def CalcularRoll(Ay,Az):
    return np.arctan2(Ay, Az)

def PrepararFila_v2(datos):
    # Pasamos la lista de listas a una matriz
    datos = np.array(datos)
    # Ahora tenemos una matriz, en el que cada fila es una muestra.
    Informacion = []
    # de la matriz sacaremos un único vector con toda la información
    # - Sensores de flexión [0-4]
    # Calcularemos la media de las filas de las 5 primeras columnas
    for i in range(0,5):
        media = np.mean(datos[:,i])
        Informacion.append(media)
    
    # Una vez obtenido las medias de los sensores de flexión, pasamos a los sensores del giroscopio
    # De aquí se obtendrán la media, la desviación típica de cada eje y de su magnitud vectorial
    
    # Acelerómetro
    # Calculamos el Pitch y el Roll y obtenemos la media
    Pitch = []
    Roll = []
    for i in range(10): # Son 10 muestras
        Ax = datos[i,5]
        Ay = datos[i,6]
        Az = datos[i,7]
        Pitch.append(CalcularPitch(Ax,Ay,Az))
        Roll.append(CalcularRoll(Ay,Az))
    
    # Para evitar los picos, calculamos la mediana en vez de la media
    Informacion.append(np.median(Pitch))
    Informacion.append(np.median(Roll))
    
    # - Media y desviación estándar de la magnitud vectorial (sqrt(Ax^2 + Ay^2 + Az^2))
    Amag = []
    for i in range(0,10):
        Amag.append(np.sqrt((np.square(datos[i,5])) + (np.square(datos[i,6])) + (np.square(datos[i,7]))))
    media = np.mean(Amag)
    desv = np.std(Amag)
    Informacion.append(media)
    Informacion.append(desv)
        
    # - Media y desviación estándar de la magnitud vectorial (sqrt(Gx^2 + Gy^2 + Gz^2))
    Gmag = []
    for i in range(0,10):
        Gmag.append(np.sqrt((np.square(datos[i,8])) + (np.square(datos[i,9])) + (np.square(datos[i,10]))))
    media = np.mean(Gmag)
    desv = np.std(Gmag)
    Informacion.append(media)
    Informacion.append(desv)
    
    # Pasamos los datos a float
    Informacion = [float(x) for x in Informacion]
    
    return Informacion

def PrepararFila_v3(datos):
    datos = np.array(datos)
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
    arr_info = np.array(Informacion)

    error = np.any((arr_info == 4095.0) | (arr_info == 0.0))
    return [float(x) for x in Informacion],error