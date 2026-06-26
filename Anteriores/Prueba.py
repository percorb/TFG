import serial
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

# ===== dataset =====
df = pd.read_csv("dataset_total.csv")

X = df.drop(columns=["Label"]).values
y = df["Label"].values

# ===== scaler =====
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ===== KNN =====
knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X, y)

# ===== Arduino =====
arduino = serial.Serial('COM6', 115200)

from FuncionesLector import PrepararDatos, PrepararFila_v3

buffer = []
window = 10

print("KNN en tiempo real iniciado...")

while True:
    try:
        linea = arduino.readline().decode().strip()
        data = linea.split(',')

        if len(data) != 11:
            continue

        buffer.append(PrepararDatos(data))

        if len(buffer) == window:
            features = PrepararFila_v3(buffer)

            # FIX IMPORTANTE
            features = scaler.transform([features])

            pred = knn.predict(features)[0]

            print("Predicción:", pred)

            buffer = []

    except Exception as e:
        print("Error:", e)