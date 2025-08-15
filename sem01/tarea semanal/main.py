import csv
import os

# Nombre del archivo donde se guardarán los datos
archivo_productos = "productos.csv"
encabezados = ["Nombre", "Marca", "Cantidad", "Precio Unitario", "Total"]

# --- Función para asegurar que el archivo existe con encabezados ---
def preparar_archivo():
    # Si el archivo no existe, lo crea y escribe los encabezados.
    if not os.path.exists(archivo_productos):
        with open(archivo_productos, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(encabezados)

# --- Funciones CRUD ---

def agregar_producto():
    print("\n--- Agregar Producto ---")
    nombre = input("Nombre: ")
    marca = input("Marca: ")
    cantidad = int(input("Cantidad: "))
    precio = float(input("Precio Unitario: "))
    total = cantidad * precio

    # Abre el archivo en modo 'append' (agregar al final)
    with open(archivo_productos, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nombre, marca, cantidad, precio, total])
    
    print("Producto agregado.")

def mostrar_productos():
    print("\n--- Lista de Productos ---")
    with open(archivo_productos, mode='r', newline='') as file:
        reader = csv.reader(file)
        # Muestra cada fila con su número de línea (ID)
        for i, row in enumerate(reader):
            print(f"ID {i}: {row}")

def modificar_producto():
    mostrar_productos()
    id_modificar = int(input("\nID del producto a modificar: "))

    # Leer todos los productos en una lista
    with open(archivo_productos, mode='r', newline='') as file:
        productos = list(csv.reader(file))
    
    # Pedir nuevos datos
    print(f"Modificando: {productos[id_modificar]}")
    nombre = input("Nuevo Nombre: ")
    marca = input("Nueva Marca: ")
    cantidad = int(input("Nueva Cantidad: "))
    precio = float(input("Nuevo Precio Unitario: "))
    total = cantidad * precio

    # Actualizar la lista
    productos[id_modificar] = [nombre, marca, cantidad, precio, total]

    # Escribir la lista completa de vuelta al archivo
    with open(archivo_productos, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(productos)
    
    print("Producto modificado.")

def eliminar_producto():
    mostrar_productos()
    id_eliminar = int(input("\nID del producto a eliminar: "))

    # Leer todos los productos
    with open(archivo_productos, mode='r', newline='') as file:
        productos = list(csv.reader(file))

    # Eliminar el producto de la lista
    productos.pop(id_eliminar)

    # Escribir la lista actualizada al archivo
    with open(archivo_productos, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(productos)
    
    print("Producto eliminado.")

def buscar_producto():
    termino = input("\nIngrese nombre o marca a buscar: ")
    encontrados = False
    
    with open(archivo_productos, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader) # Saltar encabezados
        for row in reader:
            # Busca el término en el nombre (índice 0) o la marca (índice 1)
            if termino.lower() in row[0].lower() or termino.lower() in row[1].lower():
                print(f"Encontrado: {row}")
                encontrados = True
    
    if not encontrados:
        print("No se encontraron coincidencias.")


# --- Menú Principal ---
preparar_archivo() # Se asegura de que el archivo exista antes de empezar

while True:
    print("\n===== MENÚ PRINCIPAL =====")
    print("1. Ver productos")
    print("2. Agregar producto")
    print("3. Modificar producto")
    print("4. Eliminar producto")
    print("5. Buscar producto")
    print("6. Salir")
    
    opcion = input("Seleccione una opción: ")
    
    if opcion == '1':
        mostrar_productos()
    elif opcion == '2':
        agregar_producto()
    elif opcion == '3':
        modificar_producto()
    elif opcion == '4':
        eliminar_producto()
    elif opcion == '5':
        buscar_producto()
    elif opcion == '6':
        print("Adiós.")
        break
    else:
        print("Opción no válida.")