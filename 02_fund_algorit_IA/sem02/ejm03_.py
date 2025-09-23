import cv2
import numpy as np

# Captura de video (0 - cámara web)
cap = cv2.VideoCapture(0)

# Funcion auxiliar para poner titulo con sombra
def agregar_titulo(img, texto):
    img_copy = img.copy()
    # Texto negro (sombra)
    cv2.putText(img_copy, texto, (11, 26), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (0, 0, 0), 3, cv2.LINE_AA)
    # Texto blanco encima
    cv2.putText(img_copy, texto, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                0.8, (255, 255, 255), 2, cv2.LINE_AA)
    return img_copy
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Redimensionar para que todas las imagenes tengan el mismo tamaño
    frame = cv2.resize(frame, (320, 240))
    # Escalar de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Operaciones con matrices
    brillo = cv2.add(gray, 50)
    oscuro = cv2.subtract(gray, 50)
    negativo = 255 - gray
    rotado = cv2.transpose(gray)

    # Convertir a BGR para unir 
    gray_bgr = cv2.cvtColor(gray,cv2.COLOR_GRAY2BGR)
    brillo_bgr = cv2.cvtColor(brillo,cv2.COLOR_GRAY2BGR)
    oscuro_bgr = cv2.cvtColor(oscuro,cv2.COLOR_GRAY2BGR)
    negativo_bgr = cv2.cvtColor(negativo,cv2.COLOR_GRAY2BGR)
    rotado_bgr = cv2.cvtColor(rotado,cv2.COLOR_GRAY2BGR)

    # Redimensionar rotado
    rotado_bgr = cv2.resize(rotado_bgr, (320, 240))

    # Agregar titulos
    frame = agregar_titulo(frame, 'Original (Color)')
    gray_bgr = agregar_titulo(gray_bgr, 'Escala de grises')
    brillo_bgr = agregar_titulo(brillo_bgr, 'Brillo +50')
    oscuro_bgr = agregar_titulo(oscuro_bgr, 'Oscuro -50')
    negativo_bgr = agregar_titulo(negativo_bgr, 'Negativo')
    rotado_bgr = agregar_titulo(rotado_bgr, 'Rotado (transpuesta)')

    # Crear mosaico
    fila1 = np.hstack((frame, gray_bgr, brillo_bgr))
    fila2 = np.hstack((oscuro_bgr, negativo_bgr, rotado_bgr))
    mosaico = np.vstack((fila1, fila2))

    # Mostrar mosaico
    cv2.imshow('Transformaciones con Algebra Lineal', mosaico)
    # Salir con ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()