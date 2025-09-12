import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import label, median_filter

ruta = "C:\\Users\\Estudiante\\Downloads\\imgs\\platano3.png"

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('No se pudo cargar la imagen. Revisa la ruta del archivo.')

# Suavizado de la imagen
img_suave = median_filter(img, size=5)

# Detección de bordes
edge = cv2.Canny(img_suave, 50, 150)

# Detección de manchas
_, thresh = cv2.threshold(img_suave, 100, 255, cv2.THRESH_BINARY_INV)

#Etiquetar regiones con SciPy
labeled_array, num_features = label(thresh)

print(f"Número de manchas detectadas: {num_features}")

# Analizar cada mancha
areas = []
for i in range(1, num_features + 1):
    area = np.sum(labeled_array == i)
    areas.append(area)

areas = np.array(areas)
manchas_grandes = areas>10

print(f"Manchas consideras defectos: {np.sum(manchas_grandes)}")

# Visualización de los resultados
plt.figure(figsize=(12, 5)) 

plt.subplot(1, 3, 1)
plt.title('Escala de grises')
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Bordes detectados')
plt.imshow(edge, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Manchas defectuosas (area>500 pixeles)')
plt.imshow(thresh, cmap='gray')
mask=np.isin(labeled_array,np.where(manchas_grandes)[0]+1)
plt.scatter(*np.where(mask)[::-1], color='red', s=1)
plt.axis('off')

plt.tight_layout()
plt.show()