#pip install opencv-python
#pip install opencv-contrib-python
#pip install imutils
import cv2
import imutils
import numpy as np

cap=cv2.VideoCapture(0) #(0)1ra cam / (1)2da cam

while True:
    red, frame=cap.read()
    #Convertir frames a HSV para BGR
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #Definir color a detectar (tono,saturacion,brillo)
    abajo_azul=np.array([98,68,50])
    arriba_azul=np.array([121,255,255])

    mascara_azul=cv2.inRange(hsv, abajo_azul, arriba_azul)

    #Deteccion de contornos
    contorno_azul=cv2.findContours(mascara_azul,
                                    cv2.RETR_TREE,
                                    cv2.CHAIN_APPROX_SIMPLE)
    contorno_azul=imutils.grab_contours(contorno_azul)

    #Agregar formato texto
    font=cv2.FONT_HERSHEY_SIMPLEX
    thickness=2
    color_blue=(253, 251, 115) #color cian

    #Agrega el texto y el centro
    for contour in contorno_azul:
        area1=cv2.contourArea(contour)
        if area1>5000:
            cv2.drawContours(frame,[contour],0,(255,0,0),2)
            #Encontrar el centro de un area
            M=cv2.moments(contour)
            cx=int(M['m10']/M['m10'])
            cy=int(M['m01']/M['m01'])
            cv2.circle(frame,(cx,cy),7,(255,255,255),-1)
            cv2.putText(frame,'Azul',(cx,cy),
                        font,1,color_blue,
                        thickness,cv2.LINE_AA)
    cv2.imshow('mi primer video',frame)
    k=cv2.waitKey(1)
    if k==27:
        break
cap.release()
cv2.destroyAllWindows



