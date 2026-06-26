import serial # Para leer la información del Arduino
import os # Para comprobar si el archivo está vacío

from FuncionesLector import *

# Acceso al puerto serial del Arduino
arduino = serial.Serial('COM5', 115200)
Letra = "O"
file = open(f"Dataset/{Letra}.csv", "a") # Si no existe se crea, y si existe, entonces se abre para añadir información al final

if os.path.getsize(f"Dataset/{Letra}.csv") == 0: # Si el archivo está vacío, entonces se escribe la primera línea con los nombres de las columnas
    file.write("Label,Pulgar,Indice,Corazon,Anular,Mennique,Pulgar_std,Indice_std,Corazon_std,Anular_std,Mennique_std,Pitch_median,Roll_median,Pitch_range,Roll_range,A_mag_mean,A_mag_std,G_mag_mean,G_mag_std\n")
    
# ============= #
# Escribir fila #
# ============= #
# - Se encarga de separar la información y escribirla en el csv
def EscribirFila(Fila):
    cadena = ""
    for elto in Fila:
        cadena += f"{elto}"
        if elto!=Fila[len(Fila)-1]:
            cadena+=","
    file.write(Letra + ","+cadena + "\n")

# ====== #
# Lector #
# ====== #
# Recopila la información para escribirla en un csv
def Lector():
    datos = []
    
    ventana = 10 # Se trabajará con ventanas de 10 muestras
    muestras = 50 # Se escribirán 50 líneas en el csv
    
    cont = 0
    contador = 1
    input(f"Presiona enter para comenzar la lectura de {Letra}")
    while cont<muestras:
        try:
            input(f"Coloca la mano y presiona Enter")
            arduino.reset_input_buffer() # Para limpiar el buffer del serial para que coja el gesto de la mano.
            linea = arduino.readline().decode('utf-8').strip()
            data = linea.split(',')
            procesado = PrepararDatos(data) # Realiza los cálculos necesarios
            datos.append(procesado)
            if contador==ventana:
                contador=1
                Fila,error = PrepararFila_v3(datos)
                EscribirFila(Fila)
                datos = []
                file.flush()
                cont+=1
                print(f"Fila {cont}/50")
                print(Fila)
            else:
                contador+=1
        except Exception as e:
            print(f"Error: {e}")
            continue
    print("Lectura de datos finalizada")


# Llamada a la función principal
Lector()