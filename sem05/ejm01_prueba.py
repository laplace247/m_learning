# pip install tensorflow
import tensorflow as tf
import numpy as np

# ======== 1) Crear datos ========
# x de 0 a 10
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], dtype=float)
# y = 2x - 1
y = 2 * x - 1

# ======== 2) Definir el modelo ========
# Una red neuronal con 1 neurona y 1 entrada
modelo = tf.keras.Sequential([
    tf.keras.layers.Dense(units=1, input_shape=[1])
])

# ======== 3) Compilar el modelo ========
# sgd = descenso del gradiente, mse = error cuadrático medio
modelo.compile(optimizer='sgd', loss='mean_squared_error')

# ======== 4) Entrenar ========
print("Entrenando el modelo...")
historial = modelo.fit(x, y, epochs=200, verbose=0)

# ======== 5) Predicción ========
nueva_x = np.array([[10.0]]) # debe ser array 2D
prediccion = modelo.predict(nueva_x)
print("Predicción para x=10:", prediccion)