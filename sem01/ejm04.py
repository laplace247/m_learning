import numpy as np

# Leer la columna 'promedio' (segunda columna -> índice 1)
ruta = "notas.csv"

notas = np.genfromtxt(ruta, delimiter=';', skip_header=1, usecols=1)
print("Notas de los estudiantes:")
print(notas)

promedio = np.mean(notas)
desviacion = np.std(notas)
desaprobadas = notas[notas < 11]

print("Promedio general:", promedio)
print("Desviación estándar:", desviacion)
print("Notas desaprobadas:", desaprobadas)