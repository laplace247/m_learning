# Importar librerias
import csv
import os

# Nombre del archivo donde se guardarán los datos
archivo_productos = "productos.csv"
# Definimos los encabezados para el archivo CSV
encabezados = ["Nombre", "Marca", "Cantidad", "Precio Unitario", "Total"]

def inicializar_archivo():
    """Crea el archivo CSV con los encabezados si no existe."""
    if not os.path.exists(archivo_productos):
        with open(archivo_productos, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(encabezados)

def cargar_productos():
    """Lee todos los productos del archivo CSV y los devuelve como una lista de listas."""
    with open(archivo_productos, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

def guardar_productos(productos):
    """Escribe la lista completa de productos de vuelta al archivo CSV."""
    with open(archivo_productos, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(productos)

def mostrar_productos():
    """Muestra una lista formateada de todos los productos en el inventario."""
    print("\n--- REGISTRO DE PRODUCTOS ---")
    productos = cargar_productos()
    if len(productos) <= 1:
        print("No hay productos registrados.")
        return

    # Imprimir encabezados
    print(f"{'ID':<4} {'Nombre':<20} {'Marca':<15} {'Cantidad':<10} {'Precio U.':<15} {'Total':<15}")
    print("-" * 80)
    
    # Imprimir cada producto (saltando la fila de encabezados)
    for i, producto in enumerate(productos[1:], 1):
        nombre, marca, cantidad, precio, total = producto
        print(f"{i:<4} {nombre:<20} {marca:<15} {cantidad:<10} ${float(precio):<14,.2f} ${float(total):<14,.2f}")
    print("-" * 80)

def agregar_producto():
    """Solicita al usuario los datos de un nuevo producto y lo agrega al archivo."""
    print("\n--- AGREGAR NUEVO PRODUCTO ---")
    nombre = input("Nombre del producto: ")
    marca = input("Marca: ")
    
    try:
        cantidad = int(input("Cantidad: "))
        precio_unitario = float(input("Precio Unitario: "))
    except ValueError:
        print("Error: Cantidad y Precio deben ser números.")
        return

    total = cantidad * precio_unitario
    nuevo_producto = [nombre, marca, cantidad, precio_unitario, total]
    
    productos = cargar_productos()
    productos.append(nuevo_producto)
    guardar_productos(productos)
    
    print(f"\n¡Producto '{nombre}' agregado exitosamente!")

def modificar_producto():
    """Permite al usuario editar los datos de un producto existente."""
    mostrar_productos()
    productos = cargar_productos()
    if len(productos) <= 1:
        return
        
    try:
        id_modificar = int(input("\nIngrese el ID del producto que desea modificar: "))
        if not (1 <= id_modificar < len(productos)):
            print("ID inválido.")
            return
    except ValueError:
        print("Error: Ingrese un número de ID válido.")
        return

    print("\nIngrese los nuevos datos (deje en blanco para no cambiar):")
    producto_actual = productos[id_modificar]
    
    nombre = input(f"Nombre ({producto_actual[0]}): ") or producto_actual[0]
    marca = input(f"Marca ({producto_actual[1]}): ") or producto_actual[1]
    
    try:
        cantidad_str = input(f"Cantidad ({producto_actual[2]}): ")
        cantidad = int(cantidad_str) if cantidad_str else int(producto_actual[2])
        
        precio_str = input(f"Precio Unitario ({producto_actual[3]}): ")
        precio_unitario = float(precio_str) if precio_str else float(producto_actual[3])
    except ValueError:
        print("Error: Cantidad y Precio deben ser números.")
        return

    total = cantidad * precio_unitario
    productos[id_modificar] = [nombre, marca, cantidad, precio_unitario, total]
    guardar_productos(productos)
    
    print("\n¡Producto modificado exitosamente!")

def eliminar_producto():
    """Elimina un producto del registro según el ID proporcionado por el usuario."""
    mostrar_productos()
    productos = cargar_productos()
    if len(productos) <= 1:
        return

    try:
        id_eliminar = int(input("\nIngrese el ID del producto que desea eliminar: "))
        if not (1 <= id_eliminar < len(productos)):
            print("ID inválido.")
            return
    except ValueError:
        print("Error: Ingrese un número de ID válido.")
        return
        
    producto_eliminado = productos.pop(id_eliminar)
    guardar_productos(productos)
    
    print(f"\n¡Producto '{producto_eliminado[0]}' eliminado exitosamente!")

def buscar_producto():
    """Busca productos que coincidan con un término de búsqueda en nombre o marca."""
    termino = input("\nIngrese nombre o marca a buscar: ").lower()
    productos = cargar_productos()
    encontrados = []

    for producto in productos[1:]:
        if termino in producto[0].lower() or termino in producto[1].lower():
            encontrados.append(producto)
            
    if not encontrados:
        print(f"No se encontraron productos que coincidan con '{termino}'.")
    else:
        print("\n--- RESULTADOS DE LA BÚSQUEDA ---")
        print(f"{'Nombre':<20} {'Marca':<15} {'Cantidad':<10} {'Precio U.':<15} {'Total':<15}")
        print("-" * 80)
        for producto in encontrados:
            nombre, marca, cantidad, precio, total = producto
            print(f"{nombre:<20} {marca:<15} {cantidad:<10} ${float(precio):<14,.2f} ${float(total):<14,.2f}")
        print("-" * 80)

#  Menú Principal 
def main():
    inicializar_archivo() # Asegura que el archivo exista
    while True:
        print("\n===== MENÚ DE GESTIÓN DE PRODUCTOS =====")
        print("1. Ver todos los productos")
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
            print("Saliendo del programa. ¡Adiós!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

# Ejecutar el programa
if __name__ == "__main__":
    main()