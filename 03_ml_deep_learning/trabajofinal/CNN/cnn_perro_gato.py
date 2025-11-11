import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# Configuración
print("=== CNN CLASIFICADOR PERRO-GATO ===")
print(f"TensorFlow version: {tf.__version__}")

# Rutas de datos
data_entrenamiento = "./data/entrenamiento"
data_validacion = "./data/validacion"

# Verificar que existen los datos
if not os.path.exists(data_entrenamiento):
    print(f"Error: No existe {data_entrenamiento}")
    sys.exit(1)

# Parámetros
altura, longitud = 150, 150
batch_size = 32
epocas = 20
clases = 2

# Preprocesamiento con Data Augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

validation_datagen = ImageDataGenerator(rescale=1./255)

# Cargar datos
try:
    train_generator = train_datagen.flow_from_directory(
        data_entrenamiento,
        target_size=(altura, longitud),
        batch_size=batch_size,
        class_mode='binary'  # Para clasificación binaria
    )

    validation_generator = validation_datagen.flow_from_directory(
        data_validacion,
        target_size=(altura, longitud),
        batch_size=batch_size,
        class_mode='binary'
    )
    
    print(f"Clases encontradas: {train_generator.class_indices}")
    
except Exception as e:
    print(f"Error cargando datos: {e}")
    sys.exit(1)

# Crear modelo CNN
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(altura, longitud, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dropout(0.5),
    Dense(512, activation='relu'),
    Dense(1, activation='sigmoid')  # Salida binaria
])

# Compilar modelo
model.compile(
    loss='binary_crossentropy',
    optimizer=Adam(learning_rate=1e-4),
    metrics=['accuracy']
)

print("\nArquitectura del modelo:")
model.summary()

# Entrenar modelo
print("\nIniciando entrenamiento...")
try:
    history = model.fit(
        train_generator,
        steps_per_epoch=len(train_generator),
        epochs=epocas,
        validation_data=validation_generator,
        validation_steps=len(validation_generator)
    )
except Exception as e:
    print(f"Error durante entrenamiento: {e}")
    sys.exit(1)

# Guardar modelo
try:
    os.makedirs('./modelo', exist_ok=True)
    model.save('./modelo/cnn_perro_gato.h5')
    print("Modelo guardado en ./modelo/cnn_perro_gato.h5")
except Exception as e:
    print(f"Error guardando modelo: {e}")

# Función de predicción
def predecir_imagen(ruta_imagen):
    """Predice si una imagen es perro o gato"""
    try:
        img = load_img(ruta_imagen, target_size=(altura, longitud))
        x = img_to_array(img)
        x = x / 255.0
        x = np.expand_dims(x, axis=0)
        
        prediccion = model.predict(x, verbose=0)[0][0]
        
        if prediccion > 0.5:
            return f"perro (confianza: {prediccion:.2f})"
        else:
            return f"gato (confianza: {1-prediccion:.2f})"
            
    except Exception as e:
        return f"Error: {e}"

# Probar con imágenes de ejemplo
print("\n=== PRUEBAS ===")
imagenes_prueba = [
    "imgs_prueba/cat1.jpg",
    "imgs_prueba/cat2.jpg",
    "imgs_prueba/dog1.jpg", 
    "imgs_prueba/dog2.jpg"
]

for img in imagenes_prueba:
    if os.path.exists(img):
        resultado = predecir_imagen(img)
        print(f"{img}: {resultado}")

print("\n¡Entrenamiento completado!")