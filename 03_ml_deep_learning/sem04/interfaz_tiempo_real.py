import cv2
from ultralytics import YOLO
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
from PIL import Image, ImageTk
import time

class InterfazTiempoReal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Detección de Naranjas en Tiempo Real")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Variables de datos
        self.contador_sanas = 0
        self.contador_enfermas = 0
        self.naranjas_unicas = set()
        self.sanas_tiempo_real = 0
        self.enfermas_tiempo_real = 0
        
        # Configurar interfaz
        self.setup_ui()
        
        # Modelo YOLO
        ruta_model = r"C:\Users\HP\Downloads\sem02\yolov8n.pt"
        self.model = YOLO(ruta_model)
        
        # Video
        ruta_video = r"C:\Users\HP\Downloads\sem02\video\nrj_video.mp4"
        self.cap = cv2.VideoCapture(ruta_video)
        
        # Variable para el frame actual
        self.frame_actual = None
        self.fps = 0
        self.frame_count = 0
        self.start_time = time.time()
        
        self.tracking_threshold = 30
        self.running = False
        
    def setup_ui(self):
        # Configurar grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame principal con estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Header con título y logo
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="SISTEMA DE DETECCIÓN DE NARANJAS", 
                               font=("Arial", 20, "bold"))
        title_label.pack(side=tk.TOP)
        
        subtitle_label = ttk.Label(header_frame, text="Análisis de Calidad con machine learning e IA", 
                                  font=("Arial", 12, "italic"))
        subtitle_label.pack(side=tk.TOP, pady=(5, 0))
        
        # Frame para video con mejor diseño
        video_frame = ttk.LabelFrame(main_frame, text="📹 Video en Tiempo Real", padding="15")
        video_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 15))
        video_frame.grid_rowconfigure(0, weight=1)
        video_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas para video con borde
        video_canvas = tk.Canvas(video_frame, bg='black', relief='sunken', bd=2)
        video_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_label = ttk.Label(video_canvas, text="🎥 Presiona 'Iniciar' para comenzar", 
                                    font=("Arial", 14), background='black', foreground='white')
        self.video_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Panel lateral con datos
        panel_frame = ttk.Frame(main_frame)
        panel_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        panel_frame.grid_rowconfigure(1, weight=1)
        
        # Frame de estadísticas actuales
        stats_frame = ttk.LabelFrame(panel_frame, text="📊 Estadísticas Actuales", padding="15")
        stats_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Estadísticas con mejor diseño
        # Sanas actuales
        sanas_frame = tk.Frame(stats_frame, bg='#e8f5e8', relief='raised', bd=1)
        sanas_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        tk.Label(sanas_frame, text="✅ Sanas (Actual)", font=("Arial", 11, "bold"), 
                bg='#e8f5e8', fg='#2d5a2d').pack(side=tk.LEFT, padx=10, pady=5)
        self.label_sanas_actual = tk.Label(sanas_frame, text="0", font=("Arial", 16, "bold"), 
                                          bg='#e8f5e8', fg='#1a8f1a')
        self.label_sanas_actual.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Enfermas actuales
        enfermas_frame = tk.Frame(stats_frame, bg='#ffe8e8', relief='raised', bd=1)
        enfermas_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        tk.Label(enfermas_frame, text="❌ Enfermas (Actual)", font=("Arial", 11, "bold"), 
                bg='#ffe8e8', fg='#5a2d2d').pack(side=tk.LEFT, padx=10, pady=5)
        self.label_enfermas_actual = tk.Label(enfermas_frame, text="0", font=("Arial", 16, "bold"), 
                                             bg='#ffe8e8', fg='#cc0000')
        self.label_enfermas_actual.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame histórico
        historico_frame = ttk.LabelFrame(panel_frame, text="📈 Datos Históricos", padding="15")
        historico_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(historico_frame, text="Total Sanas:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.label_sanas_total = ttk.Label(historico_frame, text="0", font=("Arial", 14, "bold"), foreground="#1a8f1a")
        self.label_sanas_total.grid(row=0, column=1, sticky=tk.E, padx=(10, 0), pady=3)
        
        ttk.Label(historico_frame, text="Total Enfermas:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=3)
        self.label_enfermas_total = ttk.Label(historico_frame, text="0", font=("Arial", 14, "bold"), foreground="#cc0000")
        self.label_enfermas_total.grid(row=1, column=1, sticky=tk.E, padx=(10, 0), pady=3)
        
        # Separador
        ttk.Separator(historico_frame, orient='horizontal').grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Total general
        total_frame = tk.Frame(historico_frame, bg='#f0f8ff', relief='raised', bd=1)
        total_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        tk.Label(total_frame, text="🔢 Total Procesadas", font=("Arial", 11, "bold"), 
                bg='#f0f8ff', fg='#2d4a5a').pack(side=tk.LEFT, padx=10, pady=5)
        self.label_total = tk.Label(total_frame, text="0", font=("Arial", 14, "bold"), 
                                   bg='#f0f8ff', fg='#1a5490')
        self.label_total.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Frame de rendimiento
        perf_frame = ttk.LabelFrame(panel_frame, text="⚡ Rendimiento", padding="15")
        perf_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(perf_frame, text="FPS:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=3)
        self.label_fps = ttk.Label(perf_frame, text="0", font=("Arial", 12, "bold"), foreground="#0066cc")
        self.label_fps.grid(row=0, column=1, sticky=tk.E, padx=(10, 0), pady=3)
        
        # Panel de control mejorado
        control_frame = ttk.LabelFrame(main_frame, text="🎮 Control del Sistema", padding="15")
        control_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Botones con mejor estilo
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(expand=True)
        
        self.btn_iniciar = ttk.Button(btn_frame, text="▶️ Iniciar Detección", 
                                     command=self.iniciar_deteccion, width=20)
        self.btn_iniciar.pack(side=tk.LEFT, padx=(0, 15))
        
        self.btn_detener = ttk.Button(btn_frame, text="⏹️ Detener", 
                                     command=self.detener_deteccion, state="disabled", width=15)
        self.btn_detener.pack(side=tk.LEFT, padx=(0, 15))
        
        self.btn_reset = ttk.Button(btn_frame, text="🔄 Reiniciar", 
                                   command=self.reiniciar_contadores, width=15)
        self.btn_reset.pack(side=tk.LEFT)
        
        # Barra de estado mejorada
        status_frame = tk.Frame(main_frame, bg='#e6e6e6', relief='sunken', bd=1)
        status_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(15, 0))
        
        self.label_estado = tk.Label(status_frame, text="🔴 Estado: Sistema Detenido", 
                                    font=("Arial", 11, "bold"), bg='#e6e6e6', fg='#cc0000')
        self.label_estado.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Tiempo de ejecución
        self.label_tiempo = tk.Label(status_frame, text="⏱️ Tiempo: 00:00", 
                                    font=("Arial", 10), bg='#e6e6e6', fg='#666666')
        self.label_tiempo.pack(side=tk.RIGHT, padx=10, pady=5)
        
    def reiniciar_contadores(self):
        self.contador_sanas = 0
        self.contador_enfermas = 0
        self.naranjas_unicas = set()
        self.actualizar_interfaz()
    
    def iniciar_deteccion(self):
        self.running = True
        self.start_time = time.time()
        self.frame_count = 0
        self.btn_iniciar.config(state="disabled")
        self.btn_detener.config(state="normal")
        self.btn_reset.config(state="disabled")
        self.label_estado.config(text="🟢 Estado: Sistema Activo - Procesando...", fg='#00cc00')
        
        # Iniciar hilo de procesamiento
        self.thread = threading.Thread(target=self.procesar_video)
        self.thread.daemon = True
        self.thread.start()
        
    def detener_deteccion(self):
        self.running = False
        self.btn_iniciar.config(state="normal")
        self.btn_detener.config(state="disabled")
        self.btn_reset.config(state="normal")
        self.label_estado.config(text="🔴 Estado: Sistema Detenido", fg='#cc0000')
        
    def procesar_video(self):
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
                
            frame = cv2.resize(frame, None, fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
            results = self.model(frame, verbose=False)
            
            # Procesar detecciones
            naranjas_sanas = []
            naranjas_enfermas = []
            
            for result in results:
                for box in result.boxes:
                    cls = int(box.cls[0])
                    label = self.model.names[cls]
                    
                    if label == "orange":
                        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                        roi = frame[y1:y2, x1:x2]
                        
                        if roi.size > 0:
                            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                            
                            lower_brown = np.array([5, 50, 20])
                            upper_brown = np.array([25, 255, 100])
                            lower_black = np.array([0, 0, 0])
                            upper_black = np.array([180, 255, 50])
                            
                            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
                            mask_black = cv2.inRange(hsv, lower_black, upper_black)
                            mask_disease = cv2.bitwise_or(mask_brown, mask_black)
                            
                            disease_pixels = cv2.countNonZero(mask_disease)
                            total_pixels = roi.shape[0] * roi.shape[1]
                            
                            if disease_pixels / total_pixels > 0.15:
                                naranjas_enfermas.append(box)
                            else:
                                naranjas_sanas.append(box)
            
            # Tracking de naranjas únicas
            for box_list, tipo in [(naranjas_sanas, 'sana'), (naranjas_enfermas, 'enferma')]:
                for box in box_list:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    centro_x = int((x1 + x2) / 2)
                    centro_y = int((y1 + y2) / 2)
                    
                    es_nuevo = True
                    for naranja_existente in self.naranjas_unicas:
                        dist = ((centro_x - naranja_existente[0])**2 + (centro_y - naranja_existente[1])**2)**0.5
                        if dist < self.tracking_threshold:
                            es_nuevo = False
                            break
                    
                    if es_nuevo:
                        self.naranjas_unicas.add((centro_x, centro_y, tipo))
                        if tipo == 'sana':
                            self.contador_sanas += 1
                        else:
                            self.contador_enfermas += 1
            
            # Actualizar datos en tiempo real
            self.sanas_tiempo_real = len(naranjas_sanas)
            self.enfermas_tiempo_real = len(naranjas_enfermas)
            
            # Calcular FPS
            self.frame_count += 1
            elapsed_time = time.time() - self.start_time
            if elapsed_time > 0:
                self.fps = round(self.frame_count / elapsed_time, 1)
            
            # Dibujar detecciones en el frame
            annotated_frame = results[0].plot()
            
            # Agregar información al frame con mejor diseño
            cv2.rectangle(annotated_frame, (10, 10), (300, 120), (0, 0, 0), -1)
            cv2.rectangle(annotated_frame, (10, 10), (300, 120), (255, 255, 255), 2)
            
            cv2.putText(annotated_frame, f"Sanas: {len(naranjas_sanas)}", 
                        (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Enfermas: {len(naranjas_enfermas)}", 
                        (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(annotated_frame, f"FPS: {self.fps}", 
                        (20, 95), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            self.frame_actual = annotated_frame
            
            # Actualizar interfaz
            self.root.after(0, self.actualizar_interfaz)
            
        self.root.after(0, self.detener_deteccion)
        
    def actualizar_interfaz(self):
        # Actualizar datos
        self.label_sanas_actual.config(text=str(self.sanas_tiempo_real))
        self.label_enfermas_actual.config(text=str(self.enfermas_tiempo_real))
        self.label_sanas_total.config(text=str(self.contador_sanas))
        self.label_enfermas_total.config(text=str(self.contador_enfermas))
        self.label_total.config(text=str(self.contador_sanas + self.contador_enfermas))
        self.label_fps.config(text=str(self.fps))
        
        # Actualizar tiempo de ejecución
        if self.running:
            elapsed = int(time.time() - self.start_time)
            mins, secs = divmod(elapsed, 60)
            self.label_tiempo.config(text=f"⏱️ Tiempo: {mins:02d}:{secs:02d}")
        
        # Actualizar video
        if self.frame_actual is not None:
            frame_rgb = cv2.cvtColor(self.frame_actual, cv2.COLOR_BGR2RGB)
            
            height, width = frame_rgb.shape[:2]
            max_width = 600
            if width > max_width:
                ratio = max_width / width
                new_width = max_width
                new_height = int(height * ratio)
                frame_rgb = cv2.resize(frame_rgb, (new_width, new_height))
            
            image_pil = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(image_pil)
            
            self.video_label.config(image=image_tk)
            self.video_label.image = image_tk

        
    def ejecutar(self):
        self.root.mainloop()
        self.cap.release()

if __name__ == "__main__":
    app = InterfazTiempoReal()
    app.ejecutar()