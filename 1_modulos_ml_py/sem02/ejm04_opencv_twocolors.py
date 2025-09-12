import cv2
import imutils
import numpy as np

cap=cv2.VideoCapture(0)

while True:
    red, frame=cap.read()
    if not red:
        break

    # Convertir frames a HSV
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # Deteccion color azul

    # Definir rango de color azul en HSV
    abajo_azul=np.array([98,100,20])
    arriba_azul=np.array([125,255,255])
    
    # Crear la máscara y encontrar contornos
    mascara_azul=cv2.inRange(hsv, abajo_azul, arriba_azul)
    contorno_azul=cv2.findContours(mascara_azul, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno_azul=imutils.grab_contours(contorno_azul)

    # Dibujar contornos para el azul
    for contour in contorno_azul:
        area1=cv2.contourArea(contour)
        if area1>5000:
            cv2.drawContours(frame,[contour],0,(255,0,0),3)
            # Encontrar el centro
            M=cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                cv2.putText(frame,'Azul',(cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    #Deteccion color rojo

    # Definir rangos de color rojo en HSV (necesita dos para cubrir todo el espectro)
    abajo_rojo = np.array([170, 100, 20])
    arriba_rojo = np.array([179, 255, 255])

    mascara_rojo = cv2.inRange(hsv, abajo_rojo, arriba_rojo)
    contorno_rojo=cv2.findContours(mascara_rojo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno_rojo=imutils.grab_contours(contorno_rojo)

    # Dibujar contornos para el rojo
    for contour in contorno_rojo:
        area2=cv2.contourArea(contour)
        if area2>5000:
            cv2.drawContours(frame,[contour],0,(0,0,255),3)
            M=cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
                cv2.putText(frame,'Rojo',(cx-20,cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

    cv2.imshow('Deteccion Azul y Rojo',frame)
    
    k=cv2.waitKey(1)
    if k==27:
        break
        
cap.release()
cv2.destroyAllWindows()