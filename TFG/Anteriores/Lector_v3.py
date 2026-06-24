import serial
from FuncionesLector import *

# Versión 3 del Lector


arduino = serial.Serial('COM5', 115200)
Letra = "Base"
file = open(f"{Letra}.csv", "a")
#file.write("Label,Pulgar,Indice,Corazon,Anular,Mennique,Pulgar_std,Indice_std,Corazon_std,Anular_std,Mennique_std,Pitch_median,Roll_median,Pitch_range,Roll_range,A_mag_mean,A_mag_std,G_mag_mean,G_mag_std\n")

def EscribirFila(Fila):
    cadena = ""
    for elto in Fila:
        cadena += f"{elto}"
        if elto!=Fila[len(Fila)-1]:
            cadena+=","
    file.write(Letra + ","+cadena + "\n")

def Lector():
    datos = []

    contador = 1
    maximo = 10 # Se trabajará con ventanas de 15 muestras
    muestras = 50
    cont = 0
    input(f"Presiona cuando estés listo para obtener 50 muestras de la {Letra}")
    while cont<muestras:
        try:
            input(f"Muestra {cont}/50 lista. Coloca la mano y presiona Enter")
            arduino.reset_input_buffer()
            linea = arduino.readline().decode('utf-8').strip()
            data = linea.split(',')
            procesado = PrepararDatos(data)
            datos.append(procesado)
            if contador==maximo:
                contador=0
                Fila,error = PrepararFila_v3(datos)
                datos = []
                EscribirFila(Fila)
                file.flush()
                cont+=1
                print(Fila)
                
            else:
                contador+=1
        except Exception as e:
            print(f"Error: {e}")
            continue
    print(f"Ya hemos terminado, la información se ha guardado en {Letra}.csv")

Lector()