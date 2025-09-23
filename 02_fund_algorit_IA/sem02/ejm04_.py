import cv2
import numpy as np

# Cargar desde camara (0 - cámara web)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # -- Convertir de BGR a HSV --
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # -- Rango de color verde en HSV --
    # (estos valores se puede ajustar segun la iluminacion real)
    verde_bajo = np.array([35, 40, 40]) # tono, saturación, valor
    verde_alto = np.array([85, 255, 255])

    # -- Crear mascara para extraer verdes --
    mask = cv2.inRange(hsv, verde_bajo, verde_alto)

    # -- Aplicar mascara a la imagen original --
    resultado = cv2.bitwise_and(frame, frame, mask=mask)

    # -- Mostrar ventanas --
    cv2.imshow("Original", frame)
    cv2.imshow("Verde Detectado", resultado)
    cv2.imshow("Mascara", mask)

    # Salir con ESC
    if cv2.waitKey(30) == 27:
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()