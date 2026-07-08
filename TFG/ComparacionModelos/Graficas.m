tabla = readtable("resultados.csv");

% Nombres de los modelos
modelos = tabla.Modelo;

% Accuracy
accuracy = tabla.Accuracy;
accuracy_std = tabla.Accuracy_STD;

% Tiempo de entrenamiento
train = tabla.("Train_Time_s_");
train_std = tabla.("Train_Time_STD");

% Tiempo de predicción
predict = tabla.("Predict_Time_s_");
predict_std = tabla.("Predict_Time_STD");

% F1_score
f1 = tabla.F1;
f1_std = tabla.F1_STD;

% Gráfica de comparación de modelos de machine learning
figure

bar(f1)
hold on

errorbar(1:length(f1), f1, f1_std, 'k.', 'LineWidth', 1.5)

xticks(1:length(modelos));
xticklabels(modelos);
xtickangle(20)

ylabel("F1-score");
xlabel("Modelo");
title("Comparación de F1-score entre modelos");

grid on;