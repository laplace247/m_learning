import cv2
from ultralytics import YOLO
import numpy as np

ruta_model=r"C:\Users\Estudiante\Downloads\sem02\yolov8n.pt"

model=YOLO(ruta_model)

#Ruta de Video
ruta_video=r"C:\Users\Estudiante\Downloads\sem02\video\nrj_video.mp4"

# Contadores y tracking
contador_sanas = 0
contador_enfermas = 0
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
    naranjas_sanas=[]
    naranjas_enfermas=[]

    for result in results:
        for box in result.boxes:
            cls=int(box.cls[0])
            label=model.names[cls]

            if label=="orange":
                # Extraer región de la naranja
                x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
                roi = frame[y1:y2, x1:x2]
                
                if roi.size > 0:
                    # Convertir a HSV para análisis de color
                    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    
                    # Detectar manchas oscuras/marrones (indicadores de plaga)
                    lower_brown = np.array([5, 50, 20])
                    upper_brown = np.array([25, 255, 100])
                    
                    # Detectar manchas negras
                    lower_black = np.array([0, 0, 0])
                    upper_black = np.array([180, 255, 50])
                    
                    # Crear máscaras para detectar enfermedad
                    mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
                    mask_black = cv2.inRange(hsv, lower_black, upper_black)
                    
                    # Combinar máscaras de enfermedad
                    mask_disease = cv2.bitwise_or(mask_brown, mask_black)
                    
                    # Contar píxeles de enfermedad
                    disease_pixels = cv2.countNonZero(mask_disease)
                    total_pixels = roi.shape[0] * roi.shape[1]
                    
                    # Si más del 15% tiene manchas, está enferma
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
            
            # Verificar si es una naranja nueva
            es_nuevo = True
            for naranja_existente in naranjas_unicas:
                dist = ((centro_x - naranja_existente[0])**2 + (centro_y - naranja_existente[1])**2)**0.5
                if dist < tracking_threshold:
                    es_nuevo = False
                    break
            
            if es_nuevo:
                naranjas_unicas.add((centro_x, centro_y, tipo))
                if tipo == 'sana':
                    contador_sanas += 1
                else:
                    contador_enfermas += 1
    
    # Mostrar contadores
    cv2.putText(frame, f"Sanas (tiempo real): {len(naranjas_sanas)}", 
                (20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0,255,0), 2)  # Verde
    cv2.putText(frame, f"Enfermas (tiempo real): {len(naranjas_enfermas)}", 
                (20,70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0,0,255), 2)  # Rojo
    cv2.putText(frame, f"Sanas (historico): {contador_sanas}", 
                (20,100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0,150,0), 2)  # Verde oscuro
    cv2.putText(frame, f"Enfermas (historico): {contador_enfermas}", 
                (20,130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 
                (0,0,150), 2)  # Rojo oscuro

    #Dibujar cuadro
    annotated_frame=results[0].plot()

    #Mostrar img con direcciones
    cv2.imshow("Deteccion", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()