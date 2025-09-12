# pip install pillow
# pip install tk
import cv2, tkinter as tk
from PIL import Image,ImageTk

cap, running=None, False

def mostrar_video():
  if running:
    ret, frame=cap.read()
    if ret:
      img=ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)))
      video.imgtk=img
      video.config(image=img)
    video.after(10,mostrar_video)

def iniciar():
  global cap, running
  cap,running=cv2.VideoCapture(0),True
  mostrar_video()

def detener():
  global cap, running
  running=False
  if cap: cap.release()
  video.config(image='')

root = tk.Tk()
root.title("Camara en formulario Tkinter")

# Agregar un label tipo titulo
titulo=tk.Label(root,text="Detección de Movimiento",
                font=("Arial",18,"bold"), fg="blue")
titulo.pack(pady=10)

video=tk.Label(root)
video.pack()

frame_botones=tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Iniciar",command=iniciar,width=12).grid(row=0,column=0,padx=5)
tk.Button(frame_botones, text="Detener",command=detener,width=12).grid(row=0,column=1,padx=5)

root.mainloop()