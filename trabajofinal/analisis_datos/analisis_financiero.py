# pip install pandas numpy matplotlib seaborn scikit-learn tensorflow kaggle

# IMPORTACIÓN DE LIBRERÍAS Y CONFIGURACIÓN
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
import zipfile

# Importar la API de Kaggle para la descarga
from kaggle.api.kaggle_api_extended import KaggleApi

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

print("Librerías importadas correctamente.")

# Definir un directorio local para guardar los datos
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# DESCARGA Y CARGA DE DATOS
print("\n--- Fase 1: Descargando y cargando el dataset de Noticias... ---")

# Autenticar y descargar el dataset usando la API de Kaggle
api = KaggleApi()
api.authenticate()
api.dataset_download_files('aaron7sun/stocknews', path=DATA_DIR, unzip=True)

print(f"Dataset descargado y descomprimido en la carpeta: {DATA_DIR}")

# Cargar el CSV en un DataFrame de Pandas
csv_path = os.path.join(DATA_DIR, 'Combined_News_DJIA.csv')
df = pd.read_csv(csv_path)
print("Dataset cargado exitosamente.")

# PREPROCESAMIENTO NLP Y ANÁLISIS EXPLORATORIO DE DATOS (EDA)
print("\n--- Fase 2: Procesando texto y realizando EDA... ---")

# Combinar los 25 titulares en una sola cadena de texto por fila
headlines = []
for row in range(0, len(df.index)):
    daily_headline = ' '.join(str(x) for x in df.iloc[row, 2:27])
    headlines.append(daily_headline)
df['Combined_Headlines'] = headlines

# Limpiar el texto
def clean_text(text):
    text = text.lower()
    text = re.sub('[^a-zA-Z]', ' ', text)
    return text
df['Cleaned_Headlines'] = df['Combined_Headlines'].apply(clean_text)
print("Titulares combinados y limpios.")

# Gráfico 1: Balance de Clases
plt.figure(figsize=(8, 6))
sns.countplot(x='Label', data=df)
plt.title('Balance de Clases (0: Baja/Neutral, 1: Sube)')
plt.xlabel('Clase')
plt.ylabel('Cantidad de Días')
print("\nMostrando gráfico de Balance de Clases... (Cierra la ventana para continuar)")
plt.show()
print(df['Label'].value_counts())

# PREPARACIÓN PARA MODELADO
print("\n--- Fase 3: Preparando datos para los modelos... ---")

# Dividir los datos cronológicamente
train_df = df[df['Date'] < '2015-01-01']
test_df = df[df['Date'] > '2014-12-31']

# Vectorización TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(2, 2))
X_train_tfidf = vectorizer.fit_transform(train_df['Cleaned_Headlines'])
X_test_tfidf = vectorizer.transform(test_df['Cleaned_Headlines'])

y_train = train_df['Label']
y_test = test_df['Label']
print(f"Número de características (bigramas) creadas por TF-IDF: {X_train_tfidf.shape[1]}")

# ENTRENAMIENTO Y EVALUACIÓN DE MODELOS
print("\n--- Fase 4: Entrenando y evaluando modelos... ---")

# Modelo 1: Random Forest
print("\nEntrenando el modelo RandomForest...")
model_rf = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=42)
model_rf.fit(X_train_tfidf, y_train)
predictions_rf = model_rf.predict(X_test_tfidf)
print(f"Precisión del Random Forest (Accuracy): {accuracy_score(y_test, predictions_rf):.4f}")
print("Reporte de Clasificación de Random Forest:")
print(classification_report(y_test, predictions_rf))

# Modelo 2: Red Neuronal Densa
print("\nEntrenando la Red Neuronal Densa...")
X_train_dense = X_train_tfidf.toarray()
X_test_dense = X_test_tfidf.toarray()
model_nn = Sequential([
    Dense(128, activation='relu', input_shape=(X_train_dense.shape[1],)),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])
model_nn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model_nn.fit(X_train_dense, y_train, epochs=10, batch_size=32, verbose=0)
loss, accuracy_nn = model_nn.evaluate(X_test_dense, y_test, verbose=0)
print(f"Precisión de la Red Neuronal (Accuracy): {accuracy_nn:.4f}")
predictions_nn_prob = model_nn.predict(X_test_dense)
predictions_nn = (predictions_nn_prob > 0.5).astype(int).flatten()
print("Reporte de Clasificación de la Red Neuronal:")
print(classification_report(y_test, predictions_nn))

# VISUALIZACIÓN DE RESULTADOS Y MATRICES DE CONFUSIÓN
print("\n--- Fase 5: Generando gráficos de resultados... ---")

fig, axes = plt.subplots(1, 2, figsize=(18, 7))
fig.suptitle('Matrices de Confusión de los Modelos', fontsize=16)

# Matriz para Random Forest
cm_rf = confusion_matrix(y_test, predictions_rf)
sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Baja (0)', 'Sube (1)'], yticklabels=['Baja (0)', 'Sube (1)'])
axes[0].set_title('Random Forest')
axes[0].set_xlabel('Predicho')
axes[0].set_ylabel('Real')

# Matriz para Red Neuronal Densa
cm_nn = confusion_matrix(y_test, predictions_nn)
sns.heatmap(cm_nn, annot=True, fmt='d', cmap='Greens', ax=axes[1],
            xticklabels=['Baja (0)', 'Sube (1)'], yticklabels=['Baja (0)', 'Sube (1)'])
axes[1].set_title('Red Neuronal Densa')
axes[1].set_xlabel('Predicho')
axes[1].set_ylabel('Real')

print("\nMostrando gráfico de Matrices de Confusión... (Cierra la ventana para finalizar)")
plt.show()

print("\nPROYECTO FINALIZADO!!")