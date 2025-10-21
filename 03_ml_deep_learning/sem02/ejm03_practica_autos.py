import cv2
from ultralytics import YOLO

ruta_model=r"C:\Users\Estudiante\Downloads\sem02\yolov8n.pt"

model=YOLO(ruta_model)

#Ruta de Video
ruta_video=r"C:\Users\Estudiante\Downloads\sem02\video\autos.mp4"

# Contadores y tracking
contador_historico = 0
autos_unicos = set()
tracking_threshold = 50  # Distancia mínima para considerar auto nuevo

cap = cv2.VideoCapture(ruta_video)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame=cv2.resize(frame,None,fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)
    results = model(frame, verbose=False)

    #Contar autos detectados
    autos_detectados=[]

    for result in results:
        for box in result.boxes:
            cls=int(box.cls[0])
            label=model.names[cls]

            if label=="car":
                autos_detectados.append(box)
    
    # Tracking de autos únicos
    for box in autos_detectados:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
        centro_x = int((x1 + x2) / 2)
        centro_y = int((y1 + y2) / 2)
        
        # Verificar si es un auto nuevo
        es_nuevo = True
        for auto_existente in autos_unicos:
            dist = ((centro_x - auto_existente[0])**2 + (centro_y - auto_existente[1])**2)**0.5
            if dist < tracking_threshold:
                es_nuevo = False
                break
        
        if es_nuevo:
            autos_unicos.add((centro_x, centro_y))
            contador_historico += 1
    
    # Mostrar contadores
    cv2.putText(frame, f"Autos (tiempo real): {len(autos_detectados)}", 
                (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                (0,255,0), 2)
    cv2.putText(frame, f"Autos (historico): {contador_historico}", 
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