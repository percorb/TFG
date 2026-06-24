import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ===== Cargar dataset =====
df = pd.read_csv("dataset_total.csv")

X = df.drop(columns=["Label"]).values
y = df["Label"].values

# ===== Escalado =====
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ===== División Train/Test =====
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    train_size=0.6,
    test_size=0.4,
    random_state=42,
    stratify=y
)

# ===== Entrenamiento =====
modelo = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

modelo.fit(X_train, y_train)

# ===== Predicción =====
y_pred = modelo.predict(X_test)

# ===== Precisión =====
acc = accuracy_score(y_test, y_pred)
print(f"Accuracy: {acc:.4f}")

# ===== Matriz de confusión =====
cm = confusion_matrix(y_test, y_pred)

print("\nMatriz de confusión:")
print(cm)

# ===== Mostrar gráfica =====
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=modelo.classes_
)

disp.plot(cmap="Blues")
plt.show()