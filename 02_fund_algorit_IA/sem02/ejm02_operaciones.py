import cv2
import numpy as np
from matplotlib import pyplot as plt

ruta = 'C:\\Users\\Estudiante\\Downloads\\operaciones ml\\imgs\\sonriente.png'

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

# Mostrar vector
vector = img.flatten()

# Invertir vector
vector_invertido = 255 - vector
img_invertida = vector_invertido.reshape(img.shape)

# Aumentar brillo
vector_brillo = np.clip(vector + 50, 0, 255)
img_brillo = vector_brillo.reshape(img.shape)

# Oscurecer
vector_oscuro = np.clip(vector - 100, 0, 255)
img_oscuro = vector_oscuro.reshape(img.shape)

# Mostrar resultados
plt.figure(figsize=(12, 6))

# 1 = fila, 2 = columna, 3 = índice
plt.subplot(1, 4, 1)
plt.imshow(img, cmap='gray')
plt.title('Img Original en blanco y negro')
plt.axis('off')

plt.subplot(1, 4, 2)
plt.imshow(img_invertida, cmap='gray')
plt.title('Img Invertida')
plt.axis('off')

plt.subplot(1, 4, 3)
plt.imshow(img_brillo, cmap='gray')
plt.title('Img Brillo Aumentado')
plt.axis('off')

plt.subplot(1, 4, 4)
plt.imshow(img_oscuro, cmap='gray')
plt.title('Img Oscurecida')
plt.axis('off')

# Mostrar ventana
plt.show()