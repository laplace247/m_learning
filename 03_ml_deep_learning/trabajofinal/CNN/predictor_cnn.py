import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import sys

# Configuración
altura, longitud = 150, 150
modelo_path = './modelo/cnn_perro_gato.h5'

def cargar_modelo():
    """Carga el modelo CNN entrenado"""
    try:
        if not os.path.exists(modelo_path):
            print(f"Error: No se encuentra {modelo_path}")
            print("Ejecuta primero: python cnn_perro_gato.py")
            return None
        
        modelo = tf.keras.models.load_model(modelo_path)
        print("✓ Modelo CNN cargado correctamente")
        return modelo
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None

def predecir_imagen(modelo, ruta_imagen):
    """Predice si una imagen es perro o gato"""
    try:
        if not os.path.exists(ruta_imagen):
            return f"Error: archivo {ruta_imagen} no encontrado"
        
        # Cargar y procesar imagen
        img = load_img(ruta_imagen, target_size=(altura, longitud))
        x = img_to_array(img)
        x = x / 255.0  # Normalizar
        x = np.expand_dims(x, axis=0)
        
        # Predicción
        prediccion = modelo.predict(x, verbose=0)[0][0]
        
        # Interpretar resultado (0=gato, 1=perro)
        if prediccion > 0.5:
            return f"🐕 PERRO (confianza: {prediccion:.2f})"
        else:
            return f"🐱 GATO (confianza: {1-prediccion:.2f})"
            
    except Exception as e:
        return f"Error en predicción: {str(e)}"

def main():
    """Función principal del predictor"""
    print("=== PREDICTOR CNN PERRO-GATO ===")
    
    modelo = cargar_modelo()
    if modelo is None:
        sys.exit(1)
    
    while True:
        print("\nOpciones:")
        print("1. Probar con imágenes de ejemplo")
        print("2. Predecir imagen específica")
        print("3. Salir")
        
        try:
            opcion = input("\nSelecciona (1-3): ").strip()
            
            if opcion == "1":
                # Imágenes de ejemplo
                imagenes = [
                    "Imagenes prueba/cat1.jpg",
                    "Imagenes prueba/cat2.jpg",
                    "Imagenes prueba/cat3.jpg",
                    "Imagenes prueba/dog1.jpg",
                    "Imagenes prueba/dog2.jpg",
                    "Imagenes prueba/dog3.jpg"
                ]
                
                print("\n--- RESULTADOS ---")
                for img in imagenes:
                    if os.path.exists(img):
                        resultado = predecir_imagen(modelo, img)
                        print(f"{img}: {resultado}")
                    else:
                        print(f"{img}: archivo no encontrado")
            
            elif opcion == "2":
                ruta = input("Ruta de la imagen: ").strip()
                resultado = predecir_imagen(modelo, ruta)
                print(f"\nResultado: {resultado}")
            
            elif opcion == "3":
                print("¡Hasta luego! 🐾")
                break
            
            else:
                print("Opción no válida")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego! 🐾")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()