# CAM WEB
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

ruta = r"C:\Users\Estudiante\Desktop\Sesion3otro\capturas"
#Entrenar clasificador simple
x_train = [[100],[300],[500],[700],[900],[5000],[7000],[9000],[12000]]
y_train = ['pequeno'] * 5 + ['grande'] * 4 

clf = RandomForestClassifier()
clf.fit(x_train, y_train)

#Capturar video
cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()

if not ret:
    print("No se logro acceder la camara")
    cap.release()
    exit()

frame1_gray = gray = cv2.GaussianBlur(cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY), (21,21), 0)
Conteo = 0
#Bucle principal
while True:
    ret, frame2 = cap.read()
    if not ret:
        break

    gray = cv2.GaussianBlur(cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY), (21,21), 0)
    delta = cv2.absdiff(frame1_gray, gray)
    thresh = cv2.dilate(cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1], None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    text_pred = "Sin movimientos"
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 300:
            continue
        Conteo += 1
        print("Movimiento Detectado!", Conteo)

        #Clasificar Area
        prediction = clf.predict([[area]])[0]

        #Dibujar Rectangulo
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2,(x, y), (x + w, y + h), (0, 255, 0), 2)

        #Guardar texto

        text_pred = f"{prediction} | Area: {int(area)}"
        if Conteo %80 == 0: #Hace un multiplo de 80 a los cuadros
            nombre = f"captura_{Conteo}.jpg" #Nombre del archivo junto con el nom
            direccion = os.path.join (ruta, nombre) #Une la ruta y nombre del archivo donde se va a guardar
            cv2.imwrite(direccion, frame2) #Crea una captura en la direccion y el frame de la camara
            print(f"Captura guardada{nombre}")
 
        break #Solo mostrar el primer objeto encontrado (optimiza)

    #mostrar texto en punto fijo
    cv2.putText(frame2,text_pred, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    #Mostrar video original y umbral
    cv2.imshow("Clasificacion de movimiento", frame2)
    cv2.imshow("umbral", thresh)
    
    #actualizar frame base
    frame1_gray = gray.copy()


    if cv2.waitKey(30) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()