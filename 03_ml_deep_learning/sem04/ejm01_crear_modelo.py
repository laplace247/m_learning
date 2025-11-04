import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

#Crear las clases
clases=["apple","house","cat","car","tree"]
ruta_clase=r"C:\Users\Estudiante\Downloads\sem 04\quickdraw_data"

#Cargar y procesar los datos
def cargar_datos(nombre, cantidad=1000):
    ruta=ruta_clase+"/"+nombre+".npy"
    data=np.load(ruta)
    data=data[:cantidad]
    data=data.reshape(-1,28,28,1).astype("float32")/255.0
    etiquetas=np.full((cantidad),clases.index(nombre))
    return data, etiquetas

#Cargar el dataset
x,y=[],[]
for c in clases:
    datos, etiquetas=cargar_datos(c)
    x.append(datos)
    y.append(etiquetas)

x=np.concatenate(x)
y=np.concatenate(y)

#dividir en entranamiento/prueba
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)   

#definir el modelo
modelo=tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation="relu", input_shape=(28,28,1)),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Conv2D(64, (3,3), activation="relu"),
    tf.keras.layers.MaxPooling2D((2,2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(len(clases), activation="softmax")
])

#Compilar el modelo
modelo.compile(optimizer="adam", 
               loss="sparse_categorical_crossentropy", metrics=["accuracy"])
#Entrenar el modelo
modelo.fit(x_train, y_train, epochs=30, batch_size=64, validation_split=0.1)

#Evaluar el modelo
loss, acc=modelo.evaluate(x_test, y_test)
print(f"Precision en test: {acc*100:.1f}%")

#Guardar el modelo
modelo.save(r"C:\Users\Estudiante\Downloads\sem 04\quickdraw_data\modelo_quickdraw.h5")
print("Modelo guardado")
