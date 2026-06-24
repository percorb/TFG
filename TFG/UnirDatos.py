import pandas as pd
import glob

# coger todos los CSV del directorio
csv_files = glob.glob("Dataset/*.csv")

# quitar el dataset final si existe
csv_files = [f for f in csv_files if f != "Dataset/dataset_total.csv"]

print("Archivos usados:", csv_files)

# leer y unir
df_list = [pd.read_csv(f) for f in csv_files]
df_total = pd.concat(df_list, ignore_index=True)

# guardar
df_total.to_csv("Dataset/dataset_total.csv", index=False)

print("Dataset unido correctamente")
print(df_total.shape)
print(df_total["Label"].value_counts())