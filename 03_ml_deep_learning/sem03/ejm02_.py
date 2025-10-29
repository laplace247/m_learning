#Aprendizaje no Supervizado - K Means
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

#Cargar datos
df = pd.read_csv('earthquake_data_tsunami.csv')

#Estandarizacion
x = df[["magnitude","depth","sig",]]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

#K-Means
K = 3 #Nro de grupos
kmeans = KMeans(n_clusters=K, n_init=10, random_state=42)
df["Grupo"] = kmeans.fit_predict(x_scaled)

#Mostrar datos
print("Agrupacion de terremotos")
print(f"Dataset contiene {len(df)} terremotos desde {df['Year'].min()} hasta {df['Year'].max()}")
print(df[["magnitude","depth","sig","Year","Month","Grupo"]].head(10))

#Analisis de tsunamis por grupo
print("\nAnalisis de Tsunamis por Grupo:")
for i in range(K):
    grupo_data = df[df["Grupo"] == i]
    tsunamis = grupo_data["tsunami"].sum()
    total = len(grupo_data)
    porcentaje = (tsunamis/total)*100
    print(f"Grupo {i}: {tsunamis}/{total} terremotos generaron tsunami ({porcentaje:.1f}%)")

#Visualizar graficos
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))

#Grafico de dispersion
ax1.scatter(df["magnitude"], df["depth"], c=df["Grupo"], cmap="rainbow", s=100)
ax1.set_title("Agrupacion de Terremotos")
ax1.set_xlabel("Magnitud")
ax1.set_ylabel("Profundidad")
ax1.grid(True)

#Grafico circular de tsunamis por grupo
porcentajes = []
labels = []
for i in range(K):
    grupo_data = df[df["Grupo"] == i]
    tsunamis = grupo_data["tsunami"].sum()
    total = len(grupo_data)
    porcentaje = (tsunamis/total)*100
    porcentajes.append(porcentaje)
    labels.append(f"Grupo {i}\n{porcentaje:.1f}%")

colors = ['blue', 'green', 'red']
ax2.pie(porcentajes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax2.set_title("Probabilidad de Tsunami por Grupo")

plt.tight_layout()
plt.show()