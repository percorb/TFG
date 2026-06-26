import socket

import serial
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

from FuncionesLector import PrepararDatos, PrepararFila_v3

# ===== Dataset =====
df = pd.read_csv("dataset_total.csv")

X = df.drop(columns=["Label"]).values
y = df["Label"].values

# ===== Escalado =====
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ===== Random Forest =====
rf = RandomForestClassifier(
    n_estimators=1000,
    random_state=42,
    n_jobs=-1
)

rf.fit(X, y)

# ==========================================
# CONEXIÓN ESP32
# ==========================================

ESP32_IP = "192.168.0.34"   # CAMBIAR a la ip de la placa
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Conectando a ESP32...")
sock.connect((ESP32_IP, PORT))
print("Conectado")

archivo = sock.makefile()

buffer = []
window = 10

print("Random Forest en tiempo real iniciado...")

while True:
    try:
        linea = archivo.readline().strip()
        
        if not linea:
            continue
        
        data = linea.split(',')

        if len(data) != 11:
            continue

        buffer.append(PrepararDatos(data))

        if len(buffer) == window:

            # Extraer características
            features = PrepararFila_v3(buffer)

            # Escalar
            features = scaler.transform([features])

            # Predicción
            pred = rf.predict(features)[0]

            # Probabilidades
            probs = rf.predict_proba(features)[0]

            # Top 3 clases más probables
            indices = np.argsort(probs)[::-1][:3]

            print(
                f"Predicción: {pred} | "
                + " | ".join(
                    f"{rf.classes_[i]}: {probs[i]:.1%}"
                    for i in indices
                )
            )

            buffer = []

    except Exception as e:
        print("Error:", e)