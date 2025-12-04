import cv2
import os

CLASES={
    0:'verdes',
    1:'fresco',
    2:'cancro',
    3:'puntos negros'
}
FOTO_POR_CLASE=30
RUTA_CLASE=r"C:\Users\Estudiante\Downloads\sem05\data"

#Crear las carpetas para las clases sin en caso no existan
for nombre_clase in CLASES.values():
    ruta_clase=os.path.join(RUTA_CLASE,nombre_clase)
    os.makedirs(ruta_clase, exist_ok=True)

#Iniciar camara
cap=cv2.VideoCapture(0) 
if not cap.isOpened():
    print("no se pudo acceder a la camara")
    exit()
print("Camara iniciada")
print("Presione 0 para guardar como VERDES, 1 para FRESCO, 2 para CANCRO, 3 para PUNTOS NEGROS")
print("Presione 'q' para salir")

contador={0:0,1:0} #Contador de fotos por clase
while True:
    ret,frame=cap.read()
    if not ret:
        print("Error al capturar el frame")
        break
    frame=cv2.flip(frame,1) #Invertir horizontalmente la captura
    cv2.imshow("Captura",frame)

    key=cv2.waitKey(1) & 0xFF
    if key==ord('q'):
        break
    
    #Guardar imagen
    if key in [ord('0'), ord('1')]:
        clase=int(chr(key))
        if contador[clase]<FOTO_POR_CLASE:
            nombre_clase=CLASES[clase]
            ruta_guardado=os.path.join(RUTA_CLASE,nombre_clase,f"{contador[clase]}.jpg")
            cv2.imwrite(ruta_guardado,frame)
            contador[clase]+=1
            print(f"Guardado {nombre_clase}: {contador[clase]}/{FOTO_POR_CLASE}")
        else:
            print(f"Ya tienes {FOTO_POR_CLASE} imagenes para '{CLASES[clase]}'")
        if all(v>=FOTO_POR_CLASE for v in contador.values()):
            print("Captura completada para todas las clases")
            break
cap.release()
cv2.destroyAllWindows()


