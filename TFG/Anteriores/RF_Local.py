# Uso de random forest en tiempo real obteniendo los datos del puerto serial
from FuncionesRF import *

# ================ #
# Preparar Dataset #
# ================ #
ruta = "Dataset/dataset_total.csv"
X,y = PrepararDataset(ruta)

# ===== Escalado =====
scaler,X = EscalarDatos(X)

# ============= #
# Random forest #
# ============= #
rf = PrepararModelo(X,y)

# ==================================== #
# Aplicación del modelo en tiempo real #
# ==================================== #
arduino = ConectarArduinoLocal()
ventana = 10

print("Iniciando predicción en tiempo real...")
PrediccionReal(arduino,ventana,rf,scaler)
