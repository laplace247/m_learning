import cv2
import numpy as np
import face_recognition
import tensorflow as tf
import os
import csv
from datetime import datetime

# ====== 1) Cargar imágenes de los estudiantes ======
path = r"C:\Users\DELL\Desktop\python\senati\4_TensorFlow_Keras\estudiantes"
#path = "estudiantes" # Carpeta con fotos de estudiantes
images = []
nombres = []

for archivo in os.listdir(path):
    img = cv2.imread(f"{path}/{archivo}")
    images.append(img)
    nombres.append(os.path.splitext(archivo)[0]) # nombre = archivo sin extensión

# Convertir a codificaciones faciales
def codificar_imagenes(imgs):
    lista_codigos = []
    for img in imgs:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        codigos = face_recognition.face_encodings(rgb)[0]
        lista_codigos.append(codigos)
    return lista_codigos

print("Codificando rostros de estudiantes...")
codigos_conocidos = codificar_imagenes(images)
print("¡Rostros codificados!")

# ====== 2) Crear archivo de asistencia ======
archivo_asistencia = r"C:\Users\DELL\Desktop\python\senati\4_TensorFlow_Keras\asistencia.csv"
#archivo_asistencia = "asistencia.csv"
with open(archivo_asistencia, "w", newline='') as f:
    escritor = csv.writer(f)
    escritor.writerow(["Nombre", "Fecha", "Hora"])

# ====== 3) Iniciar cámara ======
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar para acelerar
    img_peq = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    img_rgb = cv2.cvtColor(img_peq, cv2.COLOR_BGR2RGB)

    # Detectar rostros
    caras = face_recognition.face_locations(img_rgb)
    codigos = face_recognition.face_encodings(img_rgb, caras)

    for codigo, cara in zip(codigos, caras):
        # Comparar con rostros conocidos
        matches = face_recognition.compare_faces(codigos_conocidos, codigo)
        distancias = face_recognition.face_distance(codigos_conocidos, codigo)
        idx = np.argmin(distancias)

        if matches[idx]:
            nombre = nombres[idx].upper()

            # Escalar coordenadas de cara detectada
            y1, x2, y2, x1 = cara
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, nombre, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Registrar asistencia
            now = datetime.now()
            fecha = now.strftime("%Y-%m-%d")
            hora = now.strftime("%H:%M:%S")

            with open(archivo_asistencia, "a", newline='') as f:
                escritor = csv.writer(f)
                escritor.writerow([nombre, fecha, hora])

    cv2.imshow("Asistencia Automatica - Colegio", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()