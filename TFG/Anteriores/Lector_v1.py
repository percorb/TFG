import serial
import numpy as np
from FuncionesLector import *

# Datos -> Pulgar, índice, corazón, anular, meñique, Ax, Ay, Az, Gx, Gy, Gz
# Objetivo -> Media de sensores de flexión + [Media, desv std, min, max]

arduino = serial.Serial('COM6', 115200)
Letra = "Base"
file = open(f"{Letra}.csv", "a")
file.write("Label,Pulgar,Indice,Corazon,Anular,Mennique,Ax_mean,Ay_mean,Az_mean,Ax_std,Ay_std,Az_std,A_mag_mean,A_mag_std,Gx_mean,Gy_mean,Gz_mean,Gx_std,Gy_std,Gz_std,G_mag_mean,G_mag_std\n")

def EscribirFila(Fila):
    cadena = ""
    for elto in Fila:
        cadena += f"{elto}"
        if elto!=Fila[20]:
            cadena+=","
    file.write(Letra + ","+cadena + "\n")

def Lector():
    datos = []

    contador = 1
    maximo = 10 # Se trabajará con ventanas de 10 muestras
    muestras = 50
    cont = 0
    input(f"Presiona cuando estés listo para obtener 50 muestras de la {Letra}")
    while cont<muestras:
        try:
            linea = arduino.readline().decode('utf-8').strip()
            data = linea.split(',')
            procesado = PrepararDatos(data)
            datos.append(procesado)
            if contador==maximo:
                contador=0
                Fila = PrepararFila(datos)
                datos = []
                # Escribir en el csc, esto se hace con cadenas de texto
                EscribirFila(Fila)
                file.flush()
                cont+=1
                print(Fila)
                input(f"Muestra {cont}/50 lista. Coloca la mano y presiona Enter")
            else:
                contador+=1
        except Exception as e:
            print(f"Error: {e}")
            continue
    print(f"Ya hemos terminado, la información se ha guardado en {Letra}.csv")

Lector()