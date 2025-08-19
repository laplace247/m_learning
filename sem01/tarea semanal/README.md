# Sistema de Gestión de Productos

Un algoritmo simple y eficiente para gestionar inventario de productos usando Python y archivos CSV.

## Características

- **Agregar productos** - Registra nuevos productos con todos sus detalles
- **Ver productos** - Lista completa del inventario
- **Modificar productos** - Actualiza información existente
- **Eliminar productos** - Remueve productos del inventario
- **Buscar productos** - Encuentra productos por nombre o marca
- **Persistencia** - Datos guardados en archivo CSV

## Requisitos

- Python 3.x
- Módulos estándar: `csv`, `os`

## Instalación

1. Clona o descarga el proyecto
```bash
git clone https://github.com/laplace247/modulos_ml_py.git
```
2. Ejecuta el archivo principal:

```bash
python main.py
```

## Uso

### Menú Principal

```
===== MENÚ PRINCIPAL =====
1. Ver productos
2. Agregar producto  
3. Modificar producto
4. Eliminar producto
5. Buscar producto
6. Salir
```

### Estructura de Datos

Cada producto contiene:
- **Nombre** - Nombre del producto
- **Marca** - Marca del producto  
- **Cantidad** - Cantidad en stock
- **Precio Unitario** - Precio por unidad
- **Total** - Valor total (calculado automáticamente)

## Archivos

- `main.py` - Archivo principal con toda la lógica
- `productos.csv` - Base de datos en CSV (se crea automáticamente)

## Ejemplo de Uso

```python
# Para ejecutar el programa:
python main.py

# Seleccionar opción 2 para agregar producto:
Nombre: Laptop
Marca: Dell
Cantidad: 5
Precio Unitario: 800.50
# Total se calcula automáticamente: 4002.50
```

## Características

- **CRUD completo** - Create, Read, Update, Delete
- **Manejo de archivos** - Creación automática de CSV
- **Cálculos automáticos** - Total = Cantidad × Precio
- **Búsqueda flexible** - Por nombre o marca (case-insensitive)

## Formato CSV

```csv
Nombre,Marca,Cantidad,Precio Unitario,Total
Laptop,Dell,5,800.50,4002.50
Mouse,Logitech,10,25.99,259.90
```

## Licencia

Este proyecto es de uso libre para fines educativos.