import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # -- Rango de color verde (sano) --
    verde_bajo = np.array([35, 40, 40])
    verde_alto = np.array([85, 255, 255])
    mask_verde = cv2.inRange(hsv, verde_bajo, verde_alto)

    # -- Rango de color amarillo/marrón (posible enfermedad) --
    amarillo_bajo = np.array([15, 40, 40])
    amarillo_alto = np.array([35, 255, 255])
    mask_amarillo = cv2.inRange(hsv, amarillo_bajo, amarillo_alto)

    # -- Crear imagenes resaltadas --
    res_verde = cv2.bitwise_and(frame, frame, mask=mask_verde)
    res_amarillo = cv2.bitwise_and(frame, frame, mask=mask_amarillo)

    # -- Combinar: verde en verde, amarillo en rojo --
    salida = frame.copy()
    salida[mask_verde > 0] = (0, 255, 0) # Verde sano en verde
    salida[mask_amarillo > 0] = (0, 0, 255) # Amarillo enfermo en rojo

    # -- Mostrar ventanas --
    cv2.imshow("Original", frame)
    cv2.imshow("Plantas Analizadas", salida)
    cv2.imshow("Mascara Verde", mask_verde)
    cv2.imshow("Mascara Amarillo", mask_amarillo)

    # Salir con ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
