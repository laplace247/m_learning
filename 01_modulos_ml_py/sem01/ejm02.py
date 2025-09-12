import numpy as np

# Creamos dos arrays 1D
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print("Array A:", a)
print("Array B:", b)
print()

# Suma
print("Suma (A + B):", a + b)

# Resta
print("Resta (A - B):", a - b)

# Multiplicación elemento a elemento
print("Multiplicación (A * B):", a * b)

# División elemento a elemento
print("División (A / B):", a / b)

# Potencia elemento a elemento
print("Potencia (A ** 2):", a ** 2)

# Operaciones con escalares
print("A + 10:", a + 10)
print("B * 3:", b * 3)

# Operaciones estadísticas
print("Suma total de A:", np.sum(a))
print("Promedio de B:", np.mean(b))
print("Valor máximo de A:", np.max(a))
print("Valor mínimo de B:", np.min(b))