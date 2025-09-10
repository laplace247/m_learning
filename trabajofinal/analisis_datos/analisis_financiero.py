# IMPORTACIÓN DE LIBRERÍAS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Para el modelo de Deep Learning
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

print("Librerías importadas correctamente.")

# CARGA Y PREPARACIÓN DE DATOS
# Cargar los datos desde el archivo CSV
df = pd.read_csv('dataset1.csv')

# Vistazo inicial a los datos
print("Información del dataset:")
df.info()
print("\nPrimeras 5 filas:")
print(df.head())

# La columna 'Result' tiene valores -1 (legítimo) y 1 (phishing).
# Lo convertiremos a 0 (legítimo) y 1 (phishing) para que sea más estándar.
df['Result'] = df['Result'].map({-1: 0, 1: 1})

print("\nValores únicos en la columna 'Result' después de la conversión:", df['Result'].unique())

# ANÁLISIS EXPLORATORIO DE DATOS (EDA)
# Gráfico 1: Balance de Clases
# Para ver si tenemos una cantidad similar de sitios legítimos y de phishing.
plt.figure(figsize=(8, 6))
sns.countplot(x='Result', data=df)
plt.title('Balance de Clases (0: Legítimo, 1: Phishing)')
plt.xlabel('Clase')
plt.ylabel('Cantidad')
plt.show()
print(df['Result'].value_counts())

# Gráfico 2: Correlación de características (opcional, puede ser denso)
# Esto nos ayuda a ver si hay características fuertemente relacionadas.
# plt.figure(figsize=(20, 15))
# sns.heatmap(df.corr())
# plt.title('Mapa de Calor de Correlaciones')
# plt.show()
# Nota: Este mapa de calor puede ser difícil de leer con 32 características.

print("Visualizaciones generadas.")

# MODELO DE MACHINE LEARNING (RANDOM FOREST)
# Separar características (X) y variable objetivo (y)
X = df.drop('Result', axis=1)
y = df['Result']

# Dividir los datos: 80% para entrenamiento, 20% para prueba
# Para este problema, sí barajamos los datos (shuffle=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)

print(f"Tamaño del set de entrenamiento: {len(X_train)} filas")
print(f"Tamaño del set de prueba: {len(X_test)} filas")

# Entrenar el modelo RandomForest
model_rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1) # n_jobs=-1 usa todos los procesadores
model_rf.fit(X_train, y_train)

# Realizar predicciones
predictions_rf = model_rf.predict(X_test)

# Evaluar el modelo
accuracy_rf = accuracy_score(y_test, predictions_rf)
print(f"\nPrecisión del Random Forest (Accuracy): {accuracy_rf:.4f}")
print("Reporte de Clasificación del Random Forest:")
print(classification_report(y_test, predictions_rf))

# MODELO DE DEEP LEARNING (RED NEURONAL DENSA)
# Es crucial escalar las características para las redes neuronales
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Construir el modelo de Red Neuronal Densa (MLP)
model_nn = Sequential([
    # Capa de entrada: 32 neuronas (una por característica), función de activación 'relu'
    Dense(32, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    # Capa oculta
    Dense(16, activation='relu'),
    # Dropout para prevenir sobreajuste
    Dropout(0.2),
    # Capa de salida: 1 neurona, función 'sigmoid' para clasificación binaria
    Dense(1, activation='sigmoid')
])

# Compilar el modelo
model_nn.compile(optimizer='adam',
                 loss='binary_crossentropy', # Pérdida para clasificación binaria
                 metrics=['accuracy'])

model_nn.summary()

# Entrenar el modelo
history = model_nn.fit(X_train_scaled, y_train,
                       epochs=20, # 20 ciclos de entrenamiento
                       batch_size=32,
                       validation_split=0.1, # Usa 10% de los datos de entrenamiento para validación
                       verbose=1)

# Evaluar el modelo en el set de prueba
loss, accuracy_nn = model_nn.evaluate(X_test_scaled, y_test)
print(f"\nPrecisión de la Red Neuronal (Accuracy): {accuracy_nn:.4f}")

# Realizar predicciones
predictions_nn_prob = model_nn.predict(X_test_scaled)
predictions_nn = (predictions_nn_prob > 0.5).astype(int).flatten() # Convertir probabilidades a 0 o 1

print("Reporte de Clasificación de la Red Neuronal:")
print(classification_report(y_test, predictions_nn))

# GRÁFICO FINAL: COMPARACIÓN DE MATRICES DE CONFUSIÓN
fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('Matrices de Confusión de los Modelos')

# Matriz para Random Forest
cm_rf = confusion_matrix(y_test, predictions_rf)
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0])
axes[0].set_title('Random Forest')
axes[0].set_xlabel('Predicho')
axes[0].set_ylabel('Real')

# Matriz para Red Neuronal
cm_nn = confusion_matrix(y_test, predictions_nn)
sns.heatmap(cm_nn, annot=True, fmt='d', cmap='Greens', ax=axes[1])
axes[1].set_title('Red Neuronal Densa')
axes[1].set_xlabel('Predicho')
axes[1].set_ylabel('Real')

plt.show()