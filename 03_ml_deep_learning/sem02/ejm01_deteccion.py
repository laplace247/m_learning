import cv2
from ultralytics import YOLO

ruta_model=r"C:\Users\Estudiante\Downloads\sem02\yolov8n.pt"

model=YOLO(ruta_model)

#Ruta de Video
ruta_video=r"C:\Users\Estudiante\Downloads\sem02\video\persona1.mp4"

cap = cv2.VideoCapture(ruta_video)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,None,fx=0.3, fy=0.3, interpolation=cv2.INTER_AREA)

    results = model(frame, verbose=False)

    #Dibujar cuadro
    annotated_frame=results[0].plot()

    #Mostrar img con direcciones
    cv2.imshow("Deteccion", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()