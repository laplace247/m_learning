import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label, median_filter

ruta = "C:\\Users\\Estudiante\\Downloads\\imgs\\platano3.png"

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('No se pudo cargar la imagen')

img_suave = median_filter(img, size=5)

# Deteccion de bordes
edge = cv2.Canny(img_suave, 100, 200)

# Deteccion de manchas
manchas, _ = cv2.threshold(edge, 127, 255, cv2.THRESH_BINARY)

labeled_array, num_features = label(manchas)

print("Número de manchas detectadas:", num_features)

array=[]

for i in range(1, num_features + 1):
    mask = np.zeros(manchas.shape, dtype=np.uint8)
    mask[labeled_array == i] = 255
    array.append(mask)

print("Máscaras de manchas detectadas:", array)

plt.figure(figsize=(12, 4))  # Ajusta el tamaño de la figura

plt.subplot(1, 3, 1)
plt.title('Imagen original')
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Bordes detectados')
plt.imshow(edge, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Máscaras de manchas')
mask=np.zeros(manchas.shape, dtype=bool) 
plt.scatter(np.where(mask), color=plt.cm.nipy_spectral(i / num_features), s=1)
plt.imshow(labeled_array, cmap='nipy_spectral')
plt.axis('off')
plt.tight_layout()
plt.show()
