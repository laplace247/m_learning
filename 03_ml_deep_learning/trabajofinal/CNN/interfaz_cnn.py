import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os

class InterfazCNN:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("🐕🐱 Clasificador CNN Perro-Gato")
        self.ventana.geometry("600x500")
        self.ventana.configure(bg='#f0f0f0')
        
        self.modelo = None
        self.imagen_actual = None
        
        self.crear_interfaz()
        self.cargar_modelo()
    
    def crear_interfaz(self):
        # Título
        titulo = tk.Label(self.ventana, text="🐕🐱 CLASIFICADOR CNN", 
                         font=("Arial", 20, "bold"), bg='#f0f0f0')
        titulo.pack(pady=10)
        
        # Botón cargar imagen
        btn_cargar = tk.Button(self.ventana, text="📁 Cargar Imagen", 
                              command=self.cargar_imagen,
                              font=("Arial", 12), bg='#4CAF50', fg='white',
                              width=20, height=2)
        btn_cargar.pack(pady=10)
        
        # Frame para imagen
        self.frame_imagen = tk.Frame(self.ventana, bg='white', width=300, height=300)
        self.frame_imagen.pack(pady=10)
        self.frame_imagen.pack_propagate(False)
        
        self.label_imagen = tk.Label(self.frame_imagen, text="Selecciona una imagen", 
                                   bg='white', font=("Arial", 12))
        self.label_imagen.pack(expand=True)
        
        # Botón predecir
        self.btn_predecir = tk.Button(self.ventana, text="🔍 Analizar", 
                                     command=self.predecir,
                                     font=("Arial", 12), bg='#2196F3', fg='white',
                                     width=20, height=2, state='disabled')
        self.btn_predecir.pack(pady=10)
        
        # Resultado
        self.label_resultado = tk.Label(self.ventana, text="", 
                                       font=("Arial", 16, "bold"), bg='#f0f0f0')
        self.label_resultado.pack(pady=10)
        
        # Porcentajes
        self.label_porcentajes = tk.Label(self.ventana, text="", 
                                         font=("Arial", 12), bg='#f0f0f0')
        self.label_porcentajes.pack(pady=5)
    
    def cargar_modelo(self):
        """Carga el modelo CNN"""
        modelos = ['./modelo/modelo.h5', './modelo/cnn_perro_gato.h5']
        
        for modelo_path in modelos:
            if os.path.exists(modelo_path):
                try:
                    self.modelo = tf.keras.models.load_model(modelo_path)
                    self.label_resultado.configure(text=f"✅ Modelo cargado", fg="green")
                    return
                except Exception as e:
                    continue
        
        self.label_resultado.configure(text="❌ No hay modelo entrenado", fg="red")
        self.label_porcentajes.configure(text="Ejecuta: python cnn_perro_gato.py")
    
    def cargar_imagen(self):
        """Carga y muestra una imagen"""
        tipos = [("Imágenes", "*.jpg *.jpeg *.png *.bmp *.gif")]
        archivo = filedialog.askopenfilename(filetypes=tipos)
        
        if archivo:
            try:
                # Cargar imagen
                imagen = Image.open(archivo)
                self.imagen_actual = archivo
                
                # Redimensionar para mostrar
                imagen.thumbnail((280, 280))
                foto = ImageTk.PhotoImage(imagen)
                
                # Mostrar imagen
                self.label_imagen.configure(image=foto, text="")
                self.label_imagen.image = foto
                
                # Habilitar botón predecir
                self.btn_predecir.configure(state='normal')
                
                # Limpiar resultados anteriores
                self.label_resultado.configure(text="")
                self.label_porcentajes.configure(text="")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Error cargando imagen: {e}")
    
    def predecir(self):
        """Realiza la predicción"""
        if not self.modelo:
            self.label_resultado.configure(text="❌ Modelo no cargado", fg="red")
            return
        
        if not self.imagen_actual:
            self.label_resultado.configure(text="❌ No hay imagen", fg="red")
            return
        
        try:
            # Mostrar estado
            self.label_resultado.configure(text="🔄 Analizando...", fg="blue")
            self.label_porcentajes.configure(text="")
            self.ventana.update()
            
            # Procesar imagen (ajustar según el modelo)
            target_size = (128, 128)  # Usar 128x128 como en entrenamiento original
            img = load_img(self.imagen_actual, target_size=target_size)
            x = img_to_array(img)
            x = x / 255.0
            x = np.expand_dims(x, axis=0)
            
            # Predicción
            prediccion = self.modelo.predict(x, verbose=0)
            
            # Manejar diferentes tipos de salida del modelo
            if len(prediccion[0]) == 2:  # Salida categórica [gato, perro]
                prob_gato = prediccion[0][0] * 100
                prob_perro = prediccion[0][1] * 100
            else:  # Salida binaria [probabilidad]
                prob_binaria = prediccion[0][0]
                if prob_binaria > 0.5:
                    prob_perro = prob_binaria * 100
                    prob_gato = (1 - prob_binaria) * 100
                else:
                    prob_gato = (1 - prob_binaria) * 100
                    prob_perro = prob_binaria * 100
            
            # Determinar resultado
            if prob_perro > prob_gato:
                resultado = "🐕 PERRO"
                color = "#FF5722"
                confianza = prob_perro
            else:
                resultado = "🐱 GATO"
                color = "#9C27B0"
                confianza = prob_gato
            
            # Mostrar resultado en la interfaz
            self.label_resultado.configure(text=f"{resultado} ({confianza:.1f}%)", fg=color)
            self.label_porcentajes.configure(
                text=f"🐕 Perro: {prob_perro:.1f}%\n🐱 Gato: {prob_gato:.1f}%",
                fg="black"
            )
            
        except Exception as e:
            self.label_resultado.configure(text=f"❌ Error: {str(e)[:50]}", fg="red")
            self.label_porcentajes.configure(text="")
    
    def ejecutar(self):
        """Ejecuta la interfaz"""
        self.ventana.mainloop()

if __name__ == "__main__":
    app = InterfazCNN()
    app.ejecutar()