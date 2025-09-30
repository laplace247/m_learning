datos = []

while True:
    entrada = input("Ingrese un número (o 'fin' para terminar): ")
    if entrada.lower() == 'fin':
        break
    try:
        numero = float(entrada)
        datos.append(numero)
    except ValueError:
        print("Por favor ingrese un número válido")

if datos:
    media = sum(datos) / len(datos)
    print(f"\nDatos ingresados: {datos}")
    print(f"Promedio: {media:.2f}")
else:
    print("No se ingresaron datos")