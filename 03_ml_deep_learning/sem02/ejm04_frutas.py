import cv2
from ultralytics import YOLO

ruta_model=r"C:\Users\Estudiante\Downloads\sem02\yolov8n.pt"

model=YOLO(ruta_model)

#Ruta de Video
ruta_video=r"C:\Users\Estudiante\Downloads\sem02\video\nrj_video.mp4"

# Contadores y tracking
contador_historico = 0
naranjas_unicas = set()
tracking_threshold = 30  # Distancia mínima para considerar naranja nueva

cap = cv2.VideoCapture(ruta_video)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,None,fx=0.6, fy=0.6, interpolation=cv2.INTER_AREA)
    results = model(frame, verbose=False)

    #Contar naranjas detectadas
    naranjas_detectadas=[]

    for result in results:
        for box in result.boxes:
            cls=int(box.cls[0])
            label=model.names[cls]

            if label=="orange":
                naranjas_detectadas.append(box)
    
    # Tracking de naranjas únicas
    for box in naranjas_detectadas:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)
        
        # Verificar si es una naranja nueva
        es_nuevo = True
        for naranja_existente in naranjas_unicas:
            dist = ((centro_x - naranja_existente[0])**2 + (centro_y - naranja_existente[1])**2)**0.5
            if dist < tracking_threshold:
                es_nuevo = False
                break
        
        if es_nuevo:
            naranjas_unicas.add((centro_x, centro_y))
            contador_historico += 1
    
    # Mostrar contadores
    cv2.putText(frame, f"Naranjas (tiempo real): {len(naranjas_detectadas)}", 
                (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                (0,255,0), 2)
    cv2.putText(frame, f"Naranjas (historico): {contador_historico}", 
                (20,80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                (255,0,0), 2)

    #Dibujar cuadro
    annotated_frame=results[0].plot()

    #Mostrar img con direcciones
    cv2.imshow("Deteccion", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()