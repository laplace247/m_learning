import csv
import os

archivo = "notas.csv"

# Crear archivo con encabezados si no existe
if not os.path.exists(archivo):
    with open(archivo, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["estudiante", "promedio"])

def mostrar_notas():
    print("\n LISTA DE NOTAS")
    with open(archivo, mode="r", newline="") as f:
        reader = csv.reader(f, delimiter=';')
        for i, row in enumerate(reader):
            if len(row) < 2: continue # Evita filas vacías o corruptas
            if i != 0:
                print(f"{i}. {row[0]} - {row[1]}")
            else:
                print(f"Encabezados: {row}")

def agregar_nota():
    nombre = input("Nombre del estudiante: ")
    promedio = input("Nota promedio: ")
    with open(archivo, mode="a", newline="") as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow([nombre, promedio])
    print("Nota agregada correctamente.")

def eliminar_nota():
    mostrar_notas()
    fila = int(input("Número de fila a eliminar (no incluyas encabezado = fila 0): "))
    
    with open(archivo, mode="r", newline="") as f:
        lines = list(csv.reader(f, delimiter=';'))
    
    if 1 <= fila < len(lines):
        eliminado = lines.pop(fila)
        with open(archivo, mode="w", newline="") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerows(lines)
        print(f"Registro eliminado: {eliminado[0]} - {eliminado[1]}")
    else:
        print("Índice inválido. Intenta nuevamente.")

# Menú principal
while True:
    print("\n======== CRUD DE NOTAS ========")
    print("1. Ver notas")
    print("2. Agregar nota")
    print("3. Eliminar nota")
    print("4. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        mostrar_notas()
    elif opcion == "2":
        agregar_nota()
    elif opcion == "3":
        eliminar_nota()
    elif opcion == "4":
        print("Adiós.")
        break
    else:
        print("Opción no válida. Intenta nuevamente.")