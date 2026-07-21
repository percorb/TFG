from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from FuncionesRF import *

seed = 42
ruta = "./Dataset/dataset_total.csv" # La ruta es incorrecta, debe estar en la carpeta TFG

# Cargar dataset
X, y = PrepararDataset(ruta)

# Validación cruzada
cv_strategy = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=seed
)

# Modelos
modelos = {

    "Random Forest": RandomForestClassifier(random_state=seed),

    "Decision Tree": DecisionTreeClassifier(random_state=seed),

    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("modelo", LogisticRegression(random_state=seed, max_iter=1000))
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("modelo", KNeighborsClassifier())
    ]),

    "SVM": Pipeline([
        ("scaler", StandardScaler()),
        ("modelo", SVC(random_state=seed))
    ]),

    "Naive Bayes": GaussianNB()

}

# Hiperparámetros
parametros = {

    "Random Forest": {
        "n_estimators": [100, 200, 300, 600],
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5]
    },

    "Decision Tree": {
        "max_depth": [None, 10, 20],
        "min_samples_split": [2, 5, 10]
    },

    "Logistic Regression": {
        "modelo__C": [0.01, 0.1, 1, 10]
    },

    "KNN": {
        "modelo__n_neighbors": [3, 5, 7, 9],
        "modelo__weights": ["uniform", "distance"]
    },

    "SVM": {
        "modelo__C": [0.1, 1, 10],
        "modelo__kernel": ["linear", "rbf"]
    },

    "Naive Bayes": {
        "var_smoothing": [1e-9, 1e-8, 1e-7]
    }

}

print("Optimizando modelos...\n")

for nombre, modelo in modelos.items():

    print(f"--- {nombre} ---")

    random_search = RandomizedSearchCV(
        estimator=modelo,
        param_distributions=parametros[nombre],
        n_iter=10,
        cv=cv_strategy,
        scoring="accuracy",
        random_state=seed,
        n_jobs=-1
    )

    random_search.fit(X, y)

    print("Mejores parámetros:")
    print(random_search.best_params_)

    print(f"Accuracy: {random_search.best_score_:.4f}\n")