#pip install matplotlib
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
import pandas as pd

#Cargamos el dataset
iris=load_iris()
x,y=iris.data, iris.target

df=pd.DataFrame(x, columns=iris.feature_names)
df["especies"] =[iris.target_names[i] for i in y]

print(df.head(10))

#Visualizar grafico del dataset
plt.figure(figsize=(8,6))
for especies in iris.target_names: 
    subset=df[df["especies"]==especies]
    plt.scatter(subset["petal length (cm)"],
                subset["petal width (cm)"],
                label=especies)
plt.title('Flores iris segun el tamaño de petalos')
plt.xlabel('Largo del petalo')
plt.ylabel('Ancho del petalo') 
plt.legend()
plt.grid(True)
plt.show()