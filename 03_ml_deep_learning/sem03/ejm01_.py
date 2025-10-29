#Aprendizaje no Supervizado - K Means
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#Datos
datos={
    "Estudiante":["Ana","Edgar","Luis", "Maria","Carlos", "Rosa", "Jorge","Pedro","Silvia","Alexa"],
    "Matematica":[18,12,15,8,17,10,9,14,20,11],
    "Ciencia":[17,13,14,9,18,11,10,15,19,12],
    "Comunicacion":[16,14,13,10,18,9,11,10,20,13]
}

df=pd.DataFrame(datos)

#Estandarizacion
x=df[["Matematica","Ciencia","Comunicacion"]]
scaler=StandardScaler()
x_scaled=scaler.fit_transform(x)

#K-Means
K=3 #Nro de grupos
kmeans=KMeans(n_clusters=K, n_init=10, random_state=42)
df["Grupo"]=kmeans.fit_predict(x_scaled)

#Mostrar datos
print("Agrupacion de estudiantes")
print(df[["Estudiante","Matematica","Ciencia","Comunicacion","Grupo"]])

#Visualizar graficos
plt.figure(figsize=(7,5))
plt.scatter(df["Matematica"], df["Ciencia"], c=df["Grupo"], cmap="rainbow", s=100)
for i, nombre in enumerate(df["Estudiante"]):
    plt.text(df["Matematica"][i]+0.1, df["Ciencia"][i]+0.1, nombre)

plt.title("Agrupacion de Estudiantes por Grupo")
plt.colorbar(label="Grupo")
plt.xlabel("Matematica")
plt.ylabel("Ciencia")
plt.grid(True)
plt.show()
