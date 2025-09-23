import cv2
import numpy as np
from matplotlib import pyplot as plt

ruta = 'C:\\Users\\Estudiante\\Downloads\\operaciones ml\\imgs\\sonriente.png'

img = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)

plt.imshow(img, cmap='gray')
plt.title('Imagen Original')
plt.axis('off')
plt.show()

print(f'Mostrar matriz:')
print(img[:5, :10])

# Mostrar vector
vector = img.flatten()
print(f'Tamaño de la img:' , img.shape)
print(f'Tamaño del vector:' , vector.shape)