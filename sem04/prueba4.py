import os
import smtplib
import cv2, tkinter as tk
from tkinter import font as tkFont
from PIL import Image, ImageTk
from email.message import EmailMessage
from sklearn.ensemble import RandomForestClassifier
import threading

email_emisor = "fduilioomarquispe@gmail.com"
email_password = "rlot ybep mzur ykdr"
email_receptor = "floresquispeomar8@gmail.com"

rutas_capturas = "capturas_alerta"
movimientos_para_alerta = 80

cap = None
running = False
frame1_gray = None
conteo_movimientos = 0

x_train = [[100], [300], [500], [700], [900], [5000], [7000], [9000], [12000]]
y_train = ['pequeno'] * 5 + ['grande'] * 4
clf = RandomForestClassifier()
clf.fit(x_train, y_train)
os.makedirs(rutas_capturas, exist_ok=True)

def enviar_correo_en_hilo(ruta_imagen):
    email_thread = threading.Thread(target=enviar_correo_con_adjunto, args=(ruta_imagen,))
    email_thread.start()

def enviar_correo_con_adjunto(ruta_imagen):
    status_label.config(text="Enviando correo...")
    print(f"Preparando correo para {email_receptor}...")

    mensaje = EmailMessage()
    mensaje["From"] = email_emisor
    mensaje["To"] = email_receptor
    mensaje["Subject"] = "Alerta de Movimiento Detectado!"
    
    nombre_archivo = os.path.basename(ruta_imagen)
    mensaje.set_content(f"Se ha detectado un movimiento.\nSe adjunta la captura.")

    with open(ruta_imagen, "rb") as f:
        mensaje.add_attachment(f.read(), maintype="image", subtype="jpeg", filename=nombre_archivo)

    try:
        cliente_smtp = smtplib.SMTP('smtp.gmail.com', 587)
        cliente_smtp.starttls()
        cliente_smtp.login(email_emisor, email_password)
        cliente_smtp.send_message(mensaje)
        cliente_smtp.quit()
        print("Correo de alerta enviado exitosamente.")
        status_label.config(text=f"¡Alerta enviada! Conteo: {conteo_movimientos}")
    except Exception as e:
        print(f"ERROR: Ocurrió un error al enviar el correo: {e}")
        status_label.config(text="Error al enviar correo.")


def mostrar_alerta_captura(ruta_imagen):
    alerta_ventana = tk.Toplevel(root)
    alerta_ventana.title("¡Alerta de Captura!")

    img = Image.open(ruta_imagen)
    img_tk = ImageTk.PhotoImage(img)
    
    img_label = tk.Label(alerta_ventana, image=img_tk)
    img_label.image = img_tk 
    img_label.pack(padx=10, pady=10)

    msg_label = tk.Label(alerta_ventana, text="FOTO CAPTURADA", font=("Arial", 14, "bold"), fg="red")
    msg_label.pack(pady=10)

def actualizar_video():
    global frame1_gray, conteo_movimientos
    
    if running:
        ret, frame = cap.read()
        if not ret:
            detener()
            return

        # LOGICA DE DETECCION DE MOV
        gray = cv2.GaussianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), (21, 21), 0)
        delta = cv2.absdiff(frame1_gray, gray)
        thresh = cv2.dilate(cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        movimiento_detectado = False
        for contour in contours:
            if cv2.contourArea(contour) < 800:
                continue
            
            movimiento_detectado = True
            conteo_movimientos += 1
            
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # LOGICA DE ALERTA
            if conteo_movimientos % movimientos_para_alerta == 0 and conteo_movimientos > 0:
                nombre_foto = f"alerta_{conteo_movimientos}.jpg"
                direccion_foto = os.path.join(rutas_capturas, nombre_foto)
                cv2.imwrite(direccion_foto, frame)
                print(f"Límite alcanzado ({conteo_movimientos} mov.). Captura guardada.")
                
                mostrar_alerta_captura(direccion_foto)
                enviar_correo_en_hilo(direccion_foto)
            break

        # actualizar el estado en la interfaz
        if movimiento_detectado:
            status_label.config(text=f"Movimiento detectado | Conteo: {conteo_movimientos}")
        else:
            status_label.config(text=f"Monitoreando... | Conteo: {conteo_movimientos}")
        frame1_gray = gray.copy()

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        video_label.imgtk = img_tk
        video_label.config(image=img_tk)
        video_label.after(10, actualizar_video)

def iniciar():
    global cap, running, frame1_gray, conteo_movimientos
    
    if not running:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            status_label.config(text="Error: No se puede abrir la cámara")
            return
        
        ret, frame1 = cap.read()
        if not ret:
            status_label.config(text="Error: No se pudo leer el primer frame")
            cap.release()
            return
        
        frame1_gray = cv2.GaussianBlur(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), (21, 21), 0)
        conteo_movimientos = 0
        running = True
        btn_iniciar.config(state="disabled")
        btn_detener.config(state="normal")
        actualizar_video()

def detener():
    global cap, running
    if running:
        running = False
        btn_iniciar.config(state="normal")
        btn_detener.config(state="disabled")
        if cap:
            cap.release()
        video_label.config(image='')
        status_label.config(text="Sistema detenido.")

def on_closing():
    detener()
    root.destroy()

# interfaz grafica
root = tk.Tk()
root.title("Monitor de Vigilancia")

tkFont.Font(family="Arial", size=18, weight="bold")
tk.Label(root, text="Sistema de Detección y Alerta", font="Arial", fg="navy").pack(pady=10)

# mostrar video
video_label = tk.Label(root)
video_label.pack(padx=10, pady=5)

# mostrar estado
status_label = tk.Label(root, text="Sistema detenido.", font=("Arial", 12))
status_label.pack(pady=5)

# contenedor de btns
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_iniciar = tk.Button(frame_botones, text="Iniciar", command=iniciar, width=15, height=2)
btn_iniciar.grid(row=0, column=0, padx=10)

btn_detener = tk.Button(frame_botones, text="Detener", command=detener, width=15, height=2, state="disabled")
btn_detener.grid(row=0, column=1, padx=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
