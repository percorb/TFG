# ========================================================= #
# Lector_UI.py                                              #
# Módulo encargado de gestionar la lectura para los dataset #
# Autor: David Periñán Corbacho                             #
# ========================================================= #

import os # Para comprobar si el archivo está vacío
import threading

from serial import SerialException # Para que la UI no se bloquee

from FuncionesLector import PrepararDatos, PrepararFila_v3
from FuncionesArduino import ConectarArduinoLocal

arduino = None
file = None
ruta = None
Letra = ""
stop_event = None
pause_event = None

ultima_fila = None
muestra_actual = 0
ventana_actual = 0
finalizado = False
error = False
# =========================== #
# Información para el usuario #
# =========================== #
# Devuelve el número de la muestra actual.
def getMuestra():
    global muestra_actual
    return muestra_actual

# Devuelve la última fila escrita en el csv.
def getFila():
    global ultima_fila
    return ultima_fila

# Devuelve si el proceso de lectura ha finalizado.
def getFin():
    global finalizado
    return finalizado

# Devuelve si ha ocurrido un error durante la lectura.
def getError():
    global error
    return error

# Establece el estado de error a False.
def setError():
    global error
    error = False

# ================== #
# Preparación previa #
# ================== #
# Prepara los eventos de control, la conexión con el Arduino y el archivo csv para la escritura de datos.
def inicializar():
    global arduino, file, ruta, stop_event, pause_event, Letra
    # ================= # 
    # Control de estado #
    # ================= #
    stop_event = threading.Event()
    pause_event = threading.Event()
    pause_event.set() # Empieza en modo activo
    
    # ====== #
    # Serial #
    # ====== #
    # Acceso al puerto serial del Arduino
    arduino = ConectarArduinoLocal()


    # ============= #
    # Configuración #
    # ============= #
    ruta = f"Dataset/{Letra}.csv"

    file = open(ruta, "a") # Si no existe se crea, y si existe, entonces se abre para añadir información al final

    if os.path.getsize(ruta) == 0: # Si el archivo está vacío, entonces se escribe la primera línea con los nombres de las columnas
        file.write("Label,Pulgar,Indice,Corazon,Anular,Mennique,Pulgar_std,Indice_std,Corazon_std,Anular_std,Mennique_std,Pitch_median,Roll_median,Pitch_range,Roll_range,A_mag_mean,A_mag_std,G_mag_mean,G_mag_std\n")
    
# ============= #
# Escribir fila #
# ============= #
# Se encarga de separar la información y escribirla en el csv
def EscribirFila(Fila):
    global file, Letra
    file.write(Letra + "," + ",".join(map(str, Fila)) + "\n")

# ====== #
# Lector #
# ====== #
# Recopila la información para escribirla en un csv
def Lector():
    global arduino, stop_event, pause_event, file, muestra_actual, ventana_actual, ultima_fila, finalizado, error
    finalizado = False
    
    datos = []
    
    ventana = 10 # Se trabajará con ventanas de 10 muestras
    muestras = 150 # Se escribirán 150 líneas en el csv
    
    muestra_actual = 0
    ventana_actual = 1
    
    stop_event.clear()
    
    print("Inicio de lectura")
    arduino.reset_input_buffer()
    while muestra_actual<muestras and not stop_event.is_set():
        # Pausa entre las iteraciones
        
        try:
            arduino.reset_input_buffer() # Limpieza del buffer serial
            linea = arduino.readline().decode('utf-8').strip()
            
            if not linea:
                continue
            
            data = linea.split(',')
            
            procesado = PrepararDatos(data) # Realiza los cálculos necesarios
            datos.append(procesado)
            
            if ventana_actual==ventana:
                ventana_actual=1
                
                Fila,error = PrepararFila_v3(datos)
                if error:
                    arduino.close()
                    return
                EscribirFila(Fila)
                
                datos = []
                file.flush()
                
                muestra_actual+=1
                print(f"Fila {muestra_actual}/150")
                ultima_fila = Fila
                print(Fila)
                # Pausa hasta que se indique continuar
                # Para que no se almacene basura, se limpia el buffer cada vez que el usuario pulsa continuar.
                pause_event.clear()
                pause_event.wait()
                
            else:
                ventana_actual+=1
        except SerialException:
            print("El Arduino se ha desconectado.")
            error = True
            arduino.close()
            return        
        
        except Exception as e:
            print(f"Error: {e}")
            continue
    print("Lectura de datos finalizada")
    finalizado = True
    arduino.close()
# =========================== #
# Control externo desde la UI #
# =========================== #
# Prepara el entorno y lanza un hilo con el proceso de lectura.
def IniciarLectura():
    inicializar()
    threading.Thread(target=Lector, daemon=True).start()

# Acción del botón de continuar lectura. Se activa el evento de pausa para que el hilo de lectura continúe.
def ContinuarLectura():
    global pause_event
    pause_event.set()

# Finaliza el proceso de lectura
def PararLectura():
    global stop_event, pause_event
    stop_event.set()
    pause_event.set()

# Establece la letra que se va a utilizar para el nombre del archivo csv y para la columna "Label".
def setLetra(letra):
    global Letra
    Letra = letra
    print(f"Letra seleccionada {Letra}")