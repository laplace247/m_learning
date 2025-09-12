import numpy as np
import urllib.request # Permite trabajar con enlaces web

# URL del CSV exportado desde Google Sheets
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSNtdDRtpjj4b4INDL3nb'

# Descargar y leer datos directamente desde la web
response = urllib.request.urlopen(url)
data = np.genfromtxt(response, delimiter=',', skip_header=1, usecols=1)

# Procesar los datos
promedio = np.mean(data)
desviacion = np.std(data)
desaprobadas = data[data < 11]

print("Promedio general:", promedio)
print("Desviación estándar:", desviacion)
print("Notas desaprobadas:", desaprobadas)