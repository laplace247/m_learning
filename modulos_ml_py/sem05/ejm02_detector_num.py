# tensorflow.keras + OpenCV + deteccion_numeros.py
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

# ======== 1) Entrenar un modelo simple con MNIST ========
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizar y adaptar formato
x_train = x_train.reshape(-1, 28, 28, 1).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype("float32") / 255.0

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(100, activation='relu'),
    Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=2, validation_data=(x_test, y_test))

# ======== 2) Capturar imagen con OpenCV ========
cap = cv2.VideoCapture(0)

print("Presiona 'q' para salir...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Dibujar un rectangulo donde escribir el numero
    cv2.rectangle(frame, (100,100), (300,300), (0,255,0), 2)
    roi = gray[100:300, 100:300]

    # Preprocesar ROI para el modelo
    img_resized = cv2.resize(roi, (28,28))
    img_resized = cv2.bitwise_not(img_resized) # invertir: fondo negro, numero blanco
    img_resized = img_resized.astype("float32") / 255.0
    img_resized = img_resized.reshape(1,28,28,1)

    # Predicción con Tensorflow
    prediction = model.predict(img_resized, verbose=0)
    digit = np.argmax(prediction)

    # Mostrar resultado en pantalla
    cv2.putText(frame, f"Prediccion: {digit}", (100,90), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0,0,255), 2, cv2.LINE_AA)
    
    cv2.imshow("Deteccion de Digito - TensorFlow + OpenCV", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()