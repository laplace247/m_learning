import cv2
import matplotlib.pyplot as plt
from scipy import ndimage

ruta = "C:\\Users\\Estudiante\\Downloads\\imgs\\paisaje.jpg"

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('No se pudo cargar la imagen')
# Aplicar filtro Gaussiano con SciPy y OpenCV
img_scipy = ndimage.gaussian_filter(img, sigma=10)
img_cv2 = cv2.GaussianBlur(img, (0, 0), sigmaX=3)

plt.figure(figsize=(12, 4))  # Ajusta el tamaño de la figura

plt.subplot(1, 3, 1)
plt.title('Imagen original')
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.title('Filtro Gaussiano (SciPy)')
plt.imshow(img_scipy, cmap='gray')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.title('Filtro Gaussiano (OpenCV)')
plt.imshow(img_cv2, cmap='gray')
plt.axis('off')

plt.show()