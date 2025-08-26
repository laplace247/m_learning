#pip install scipy
import cv2
import matplotlib.pyplot as plt
import numpy as np

ruta = "C:\\Users\\Estudiante\\Downloads\\imgs\\paisaje.png"

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('No se pudo cargar la imagen')

# Detección de bordes
edges = cv2.Canny(img, 100, 200)

# Obtenemos las coordenadas
ys, xs = np.where(edges != 0)


# Graficamos los bordes
plt.figure(figsize=(8, 6))
plt.imshow(img, cmap='gray')
plt.scatter(xs, ys, s=1, c='red', label='Bordes')
plt.title('Bordes detectados')
plt.legend()
plt.show()
