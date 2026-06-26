# Uso de random forest en tiempo real obteniendo los datos del puerto serial
from sklearn.preprocessing import StandardScaler

from FuncionesRF import *

# ================ #
# Preparar Dataset #
# ================ #
ruta = "/Dataset/dataset_total.csv"
X,y = PrepararDataset(ruta)

# ===== Escalado =====
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ============= #
# Random forest #
# ============= #
rf = PrepararModelo(X,y)

# ==================================== #
# Aplicación del modelo en tiempo real #
# ==================================== #
ip = "192.168.0.34"   # CAMBIAR a la ip de la placa
arduino = ConectarArduinoWifi(ip)

ventana = 10 # La lectura se hace con ventanas de 10 muestras

print("Iniciando predicción en tiempo real...")
PrediccionReal(arduino,ventana,rf,scaler)
