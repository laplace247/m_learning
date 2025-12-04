import cv2
import os

RUTA_IMAGENES=r"C:\Users\Estudiante\Downloads\detec plaga nrj\data"
CLASES={
    0:'verdes',
    1:'fresco',
    2:'cancro',
    3:'puntos negros'
}

#Variables Globales
dibujando=False
x1,y1,x2,y2=-1,-1,-1,-1
cajas=[]
clase_actual=0

#Funcion para dibujar las cajas
def dibujar(event,x,y,flags,param):
    global x1,y1,x2,y2, dibujando,cajas

    if event==cv2.EVENT_LBUTTONDOWN:  #Dibuja con el clic izquierdo presionado
        dibujando=True
        x1,y1=x,y
    elif event==cv2.EVENT_MOUSEMOVE and dibujando:
        x2,y2=x,y
    elif event==cv2.EVENT_LBUTTONUP:
        dibujando=False
        x2,y2=x,y
        cajas.append((x1,y1,x2,y2,clase_actual))

#Función automatizada sin intervención manual
def etiquetar_imagen_automatica(ruta_imagen, clase_asignada):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se puede leer la imagen: {ruta_imagen}")
        return
    
    h, w, _ = imagen.shape
    nombre_imagen = os.path.basename(ruta_imagen)
    nombre_txt = os.path.splitext(nombre_imagen)[0] + ".txt"
    ruta_label = os.path.join(os.path.dirname(ruta_imagen), nombre_txt)
    
    # Crear etiqueta automática para toda la imagen
    with open(ruta_label, "w") as f:
        # Asignar clase a toda la imagen (caja que cubre toda la imagen)
        x_c, y_c = 0.5, 0.5  # Centro de la imagen
        ancho, alto = 1.0, 1.0  # Toda la imagen
        f.write(f"{clase_asignada} {x_c:.6f} {y_c:.6f} {ancho:.6f} {alto:.6f}\n")

#Función automatizada sin intervención manual
def etiquetar_imagen_automatica(ruta_imagen, clase_asignada):
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"No se puede leer la imagen: {ruta_imagen}")
        return
    
    h, w, _ = imagen.shape
    nombre_imagen = os.path.basename(ruta_imagen)
    nombre_txt = os.path.splitext(nombre_imagen)[0] + ".txt"
    ruta_label = os.path.join(os.path.dirname(ruta_imagen), nombre_txt)
    
    # Crear etiqueta automática para toda la imagen
    with open(ruta_label, "w") as f:
        # Asignar clase a toda la imagen (caja que cubre toda la imagen)
        x_c, y_c = 0.5, 0.5  # Centro de la imagen
        ancho, alto = 1.0, 1.0  # Toda la imagen
        f.write(f"{clase_asignada} {x_c:.6f} {y_c:.6f} {ancho:.6f} {alto:.6f}\n")

#Función Principal
def etiquetar_imagen(ruta_imagen,clase_carpeta):
    global cajas, clase_actual
    imagen=cv2.imread(ruta_imagen)
    if imagen is None:
        print("No se puede leer la imagen: {ruta_imagen}")
        return
    h,w,_=imagen.shape
    cajas=[]

    nombre_imagen=os.path.basename(ruta_imagen)
    nombre_txt=os.path.splitext(nombre_imagen)[0]+".txt"
    ruta_label=os.path.join(os.path.dirname(ruta_imagen),nombre_txt)

    cv2.namedWindow("Etiquetador Yolo")
    cv2.setMouseCallback("Etiquetador Yolo",dibujar)

    print(f"Imagen: {nombre_imagen}")
    print(f"Carpeta de clase: {clase_carpeta}")
    print("Dibuja las cajas del objeto con el mouse")
    print("Presiona 0 o 1 para cambiar de clase")
    print("Presiona S para guardar etiquetas o Q para saltar")

    while True:
        copia=imagen.copy()

        #Dibujar Cajas
        for(x1,y1,x2,y2,clase) in cajas:
            cv2.rectangle(copia,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(copia, CLASES[clase],(x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255),2)
            
        cv2.putText(copia,f"Clase actual:{CLASES[clase_actual]}",
                    (10,30),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,0),2)
        
        cv2.imshow("Etiquetador Yolo", copia)
        key=cv2.waitKey(1) & 0xFF

        if key==ord('q'):
            print("Imagen saltada")
            break
        elif key==ord('0'):
            clase_actual=0
        elif key==ord('1'):
            clase_actual=1 
        elif key==ord('s'):
            with open(ruta_label,"w") as f:
                for(x1,y1,x2,y2,clase) in cajas:
                    x_c=((x1+x2)/2)/w
                    y_c=((y1+y2)/2)/h
                    ancho=abs(x2-x1)/w
                    alto=abs(y2-y1)/h
                    f.write(f"{clase} {x_c:.6f} {y_c:.6f} {ancho:.6f} {alto:.6f}\n")
            print(f"Etiquetas guardadas en: {ruta_label}")
            break
        
    cv2.destroyAllWindows()

#Recorrer todas las imagenes automáticamente
contador_imagenes = 0
clase_automatica = 0

for carpeta in CLASES.values():
    ruta_clase=os.path.join(RUTA_IMAGENES,carpeta)
    if not os.path.exists(ruta_clase):
        continue
    for archivo in os.listdir(ruta_clase):
        if archivo.lower().endswith(".jpg"):
            # Cambiar clase cada 100 imágenes
            if contador_imagenes > 0 and contador_imagenes % 100 == 0:
                clase_automatica = (clase_automatica + 1) % len(CLASES)
            
            ruta_img=os.path.join(ruta_clase,archivo)
            etiquetar_imagen_automatica(ruta_img, clase_automatica)
            contador_imagenes += 1
            
            print(f"Procesada imagen {contador_imagenes}, clase: {CLASES[clase_automatica]}")

print("Proceso de etiquetado finalizado correctamente")
                    