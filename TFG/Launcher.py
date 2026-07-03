import os
import subprocess

# Comprobar si hay un entorno virtual creado
# Preparamos la ruta de python dentro del entorno virtual
venv_path = "appv"
python_venv = os.path.join(venv_path, "Scripts", "python.exe")

print("Comprobando si existe un entorno virtual...")

if not os.path.exists(venv_path):
    # No hay entorno virtual
    print("Creando entorno virtual con Python 3.14...")
    subprocess.run(["py", "-3.14", "-m", "venv", "appv"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    # Instalamos las dependencias
    print("Instalando las dependencias, estoy puede tardar unos minutos...")
    subprocess.run([python_venv, "-m", "pip", "install", "-r", "requisitos.txt"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Entorno virtual preparado")

# Ejecutamos la aplicación app.py
print("Ejecutando el programa...")
subprocess.run([python_venv, "app.py"],check=True)
