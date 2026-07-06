from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import pandas as pd
import numpy as np

# 2. Ahora importamos TODO lo de FuncionesRF sin usar los puntos ".."
from FuncionesRF import *

ruta = "./Dataset/dataset_total.csv"
seed = 42 # Semilla para permitir reproducibilidad de resultados

# 1. Obtener los datos del dataset
X,y = PrepararDataset(ruta)

#Scaler, X = EscalarDatos(X) # Escalamos los datos

# 2. Definimos la estrategia del cross validation K=10
cv_strategy = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed)

# 3. Elegimos las métricas que queremos calcular
metricas = ["accuracy", "precision_macro", "recall_macro","f1_macro"]

# 4. Diccionario con los modelos a comparar
modelos = {
    "Random Forest": RandomForestClassifier(random_state=seed),
    "Decision Tree": DecisionTreeClassifier(random_state=seed),
    "Logistic Regression": LogisticRegression(random_state=seed, max_iter=1000),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(random_state=seed),
    "Naive Bayes": GaussianNB()
}

Escalado = {
    "Random Forest": False,
    "Logistic Regression": True,
    "SVM": True,
    "KNN": True,
    "Decision Tree": False,
    "Naive Bayes": False
    
}

# Lista para ir guardandolos resultados
resumen = []

# 5. Ejecutamos la validación cruzada
print("Iniciando evaluación de los modelos con CV-10...")
for nombre, modelo in modelos.items():
    print(f"Evaluando {nombre}...")
    
    if Escalado[nombre]:
        _,x = EscalarDatos(X)
    else:
        x = X
    
    # Ejecutamos la validación cruzada
    resultados = cross_validate(modelo, x, y, cv=cv_strategy, scoring=metricas)
    
    # Obtenemos los datos del entrenamiento
    acc_medio = resultados["test_accuracy"].mean()
    acc_std = resultados["test_accuracy"].std()

    precision_media = resultados["test_precision_macro"].mean()
    precision_std = resultados["test_precision_macro"].std()

    recall_media = resultados["test_recall_macro"].mean()
    recall_std = resultados["test_recall_macro"].std()

    f1_media = resultados["test_f1_macro"].mean()
    f1_std = resultados["test_f1_macro"].std()
    
    train_time = resultados["fit_time"].mean()
    train_time_std = resultados["fit_time"].std()
    
    predict_time = resultados["score_time"].mean()
    predict_time_std = resultados["score_time"].std()
    
    
    
    # Guardamos la información en la lista resumen
    resumen.append({

        "Modelo": nombre,

        "Accuracy": acc_medio,
        "Accuracy_STD": acc_std,

        "Precision": precision_media,
        "Precision_STD": precision_std,

        "Recall": recall_media,
        "Recall_STD": recall_std,

        "F1": f1_media,
        "F1_STD": f1_std,

        "Train_Time(s)": train_time,
        "Train_Time_STD": train_time_std,

        "Predict_Time(s)": predict_time,
        "Predict_Time_STD": predict_time_std

    })
    
# 6. Convertimos la linea de resultados en un DataFrame de Pandas
df_resultados = pd.DataFrame(resumen)

# Guardamos la información en un CSV
ruta_csv = "./ComparacionModelos/resultados.csv"
df_resultados.to_csv(ruta_csv, index=False)

print("Proceso terminado")
print(f"Resultados guardados en: {ruta_csv}")
print("\nTabla de posiciones:")
print(df_resultados.to_string(index=False))
