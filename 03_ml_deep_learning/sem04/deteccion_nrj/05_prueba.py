from ultralytics import YOLO
import cv2
import os

#Ruta del modelo entrenado
ruta_modelo=r"C:\Users\Estudiante\Downloads\sem05\runs\detect\objetos\weights\best.pt"

#Verificamos que el archivo exista
if not os.path.exists(ruta_modelo):
    print("No se encontro archivo best.pt")
    exit()

#Cargamos el modelo
print("Cargando modelo entrenado..")
ruta_yolo=r"C:\Users\Estudiante\Downloads\sem05\yolov8n.pt"

model=YOLO(ruta_modelo)

#Iniciamos la camara
cap=cv2.VideoCapture(0)
if not cap.isOpened():
    print("No se puede acceder a la camara")
    exit()

print("Deteccion en tiempo real")
print("Presiona 'q' para salir")

while True:
    ret,frame=cap.read()
    if not ret:
        print("Error al capturar el frame")
        break

    #Realizar prediccion
    results=model.predict(source=frame, imgsz=640,conf=0.5,device='cpu',verbose=False)

    #Dibujar resultados
    annotated=results[0].plot()

    #Mostrar el video con detecciones
    cv2.imshow("Deteccion de objetos",annotated)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print("Deteccion finalizada")