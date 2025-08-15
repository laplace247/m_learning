import cv2
import numpy as np
import pandas as pd

# Rutas relativas. El CSV se guardará en la misma carpeta que el script.
ruta_csv = "colores_detectados.csv"
# La imagen debe estar en la misma carpeta que el script.
ruta_imagen = "pepe2.jpg"

# 1. Cargar imagen
imagen = cv2.imread(ruta_imagen)
if imagen is None:
    print(f"No se pudo cargar la imagen en la ruta: {ruta_imagen}")
    print("Asegúrate de que el archivo de imagen exista en la misma carpeta que tu script.")
    exit()

# 2. Convertir la imagen a espacio de color HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# 3. Definir rango para color rojo (en HSV)
rojo_bajo = np.array([170, 70, 50])   # Límite inferior
rojo_alto = np.array([180, 255, 255])  # Límite superior

# 4. Crear máscara usando NumPy
mask = cv2.inRange(hsv, rojo_bajo, rojo_alto)

# 5. Encontrar contornos (áreas rojas)
contornos, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lista para guardar resultados y recorrer contornos
resultados = []

# 6. Recorrer contornos y guardar datos en CSV
for cnt in contornos:
    area = cv2.contourArea(cnt)
    if area > 300:  # Evitar puntos muy pequeños o ruido
        x, y, w, h = cv2.boundingRect(cnt)
        # Dibujar un rectángulo rojo sobre el objeto detectado en la imagen original
        cv2.rectangle(imagen, (x, y), (x + w, y + h), (0, 0, 255), 2)
        resultados.append({"Posición_X": x, "Posición_Y": y, "Área": area})

# 7. Guardar en CSV con Pandas
if resultados:
    df = pd.DataFrame(resultados)
    df.to_csv(ruta_csv, index=False)
    print(f"Datos guardados en '{ruta_csv}'")
else:
    print("No se encontraron objetos rojos con el área mínima requerida.")


# 8. Mostrar imagen y máscara en ventanas separadas
cv2.imshow("Imagen Original", imagen)
cv2.imshow("Mascara Rojo", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Esquema HSV de referencia
# https://omes-va.com/wp-content/uploads/2019/09/gyuw4.png