#pip install scipy
import cv2
import matplotlib.pyplot as plt
from scipy import ndimage

ruta = "C:\\Users\\Estudiante\\Downloads\\imgs\\hoja.png"

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError('No se pudo cargar la imagen')

# Detección de bordes
edges = cv2.Canny(img, 100, 200)

# Obtenemos las coordenadas
ys, xs = ndimage.measurements.find_objects(edges > 0)[0]
ys_indices, xs_indices = (edges > 0)[ys, xs].nonzero()
ys_coords = ys.start + ys_indices
xs_coords = xs.start + xs_indices

# Graficamos los bordes
plt.figure(figsize=(8, 6))
plt.imshow(img, cmap='gray')
plt.scatter(xs_coords, ys_coords, s=0.5, c='red', label='Bordes')
plt.title('Bordes detectados (OpenCV + SciPy)')
plt.legend()
plt.show()
