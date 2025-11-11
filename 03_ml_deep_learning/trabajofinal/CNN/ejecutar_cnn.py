import os
import sys

def verificar_estructura():
    """Verifica la estructura de datos"""
    rutas_requeridas = [
        "./data/entrenamiento/gato",
        "./data/entrenamiento/perro",
        "./data/validacion/gato", 
        "./data/validacion/perro"
    ]
    
    print("=== VERIFICACIÓN DE DATOS ===")
    for ruta in rutas_requeridas:
        if os.path.exists(ruta):
            archivos = len([f for f in os.listdir(ruta) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
            print(f"✓ {ruta}: {archivos} imágenes")
        else:
            print(f"✗ {ruta}: NO EXISTE")
            return False
    return True

def verificar_dependencias():
    """Verifica TensorFlow"""
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__}")
        return True
    except ImportError:
        print("✗ TensorFlow no instalado")
        print("Ejecuta: pip install tensorflow")
        return False

def main():
    print("=== CNN CLASIFICADOR PERRO-GATO ===\n")
    
    # Verificaciones
    if not verificar_dependencias():
        return
    
    if not verificar_estructura():
        print("\nAsegúrate de tener imágenes en las carpetas correctas")
        return
    
    print("\nOpciones:")
    print("1. Entrenar CNN (cnn_perro_gato.py)")
    print("2. Usar predictor CNN (predictor_cnn.py)")
    print("3. Salir")
    
    while True:
        try:
            opcion = input("\nSelecciona (1-3): ").strip()
            
            if opcion == "1":
                print("Iniciando entrenamiento CNN...")
                os.system("python cnn_perro_gato.py")
            
            elif opcion == "2":
                if os.path.exists("./modelo/cnn_perro_gato.h5"):
                    os.system("python predictor_cnn.py")
                else:
                    print("Primero entrena el modelo (opción 1)")
            
            elif opcion == "3":
                print("¡Hasta luego! 🐾")
                break
            
            else:
                print("Opción no válida")
                
        except KeyboardInterrupt:
            print("\n¡Hasta luego! 🐾")
            break

if __name__ == "__main__":
    main()