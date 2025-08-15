import numpy as np

# Creamos un array
datos = np.array([10, 20, 30, 40, 50])

print("Array:", datos)
print()

# Funciones estadísticas básicas
print("Suma total:", np.sum(datos))
print("Promedio:", np.mean(datos))
print("Mediana:", np.median(datos))
print("Desviación estándar:", np.std(datos))
print("Varianza:", np.var(datos))
print("Valor máximo:", np.max(datos))
print("Valor mínimo:", np.min(datos))
print("Índice del valor máximo:", np.argmax(datos))
print("Índice del valor mínimo:", np.argmin(datos))