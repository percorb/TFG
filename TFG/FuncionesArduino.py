# ======================================================== #
# FuncionesArduino.py                                      #
# Módulo encargado de gestionar la conexión con el Arduino #
# Autor: David Periñán Corbacho                            #
# ======================================================== #

import serial, socket, threading

# Conexión con Arduino mediante el puerto serial local (USB).
def ConectarArduinoLocal():
    arduino = serial.Serial('COM6', 115200) 
    
    return arduino

# Conexión WiFi con Arduino, usando sockets.
def ConectarArduinoWifi(ip):
    # Para que funcione, el Arduino debe estar conectado a la misma red WiFi
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip,5000))
    print("Conectado")
    
    arduino = sock.makefile()
    return arduino

cancel_wifi = threading.Event() # Por si se pulsa otro botón, se cancela la conexión
# Conexión WiFi con Arduino mediante el uso de hilos para no bloquear la UI.
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
