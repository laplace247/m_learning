import cv2
import numpy as np
import tensorflow as tf

#Cargar el modelo entrenado
modelo=tf.keras.models.load_model(r"C:\Users\Estudiante\Downloads\sem 04\quickdraw_data\modelo_quickdraw.h5")

clases=["apple","house","cat","car","tree"]

#Crear el lienzo para dibujar
ancho,alto=400,400
canvas=np.ones((alto,ancho,3),dtype=np.uint8)*255
dibujando=False
color=0 #color negro
grosor=10 #nro de grosor
ultimo_punto=None

#Funcion para dibujar
def dibujar(event, x, y, flags, param):
    global dibujando, ultimo_punto
    if event==cv2.EVENT_LBUTTONDOWN:
        dibujando=True
        ultimo_punto=(x,y)
    elif event==cv2.EVENT_MOUSEMOVE and dibujando:
        cv2.line(canvas, ultimo_punto, (x,y), color, grosor)
        ultimo_punto=(x,y)
    elif event==cv2.EVENT_LBUTTONUP:
        dibujando=False

cv2.namedWindow("Dibuja Algo")
cv2.setMouseCallback("Dibuja Algo", dibujar)

print("Dibuja con el mouse y presiona ESPACIO para reconocer, C para limpiar, Q para salir")

#Bucle principal
while True:
    cv2.imshow("Dibuja Algo", canvas)
    tecla=cv2.waitKey(1) & 0XFF

    if tecla==ord("q"):
        break
    elif tecla==ord("c"):
        canvas[:]=255 #limpiar el lienzo
    elif tecla==32:
        #preprocesar la img para el modelo
        img_gray=cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
        img=cv2.resize(img_gray, (28,28))
        img=255-img
        img=img.reshape(1, 28, 28, 1).astype('float32')/255.0

        #prediccion
        pred=modelo.predict(img)
        clase=clases[np.argmax(pred)]
        confianza=np.max(pred)

        print(f"Prediccion: {clase} con {confianza*100:.2f}%")

        #mostrar prediccion
        salida=canvas.copy()
        cv2.putText(salida, f"{clase} {confianza*100:.1f}%", (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
        cv2.imshow("Dibuja Algo", salida)
        cv2.waitKey(1500)
cv2.destroyAllWindows()
