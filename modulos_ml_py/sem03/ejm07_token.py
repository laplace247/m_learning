from nltk.tokenize import TreebankWordTokenizer, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import nltk

# Descargar recursos necesarios
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

# Texto de ejemplo
texto = "El producto es excelente y me hace muy feliz, pero el servicio fue terrible."


# Tokenizacion en oraciones y palabras
tokenizer = TreebankWordTokenizer()
stop_words = set(stopwords.words("spanish"))

candidatos = []

for oracion in sent_tokenize(texto, language="spanish"):
    tokens = tokenizer.tokenize(oracion)
    for i, palabra in enumerate(tokens):
        # Regla: empieza con mayusculas y no stopword
        if palabra[0].isupper() and palabra.lower() not in stop_words:
            # Evitar la primera palabra de la oracion si no parece nombre propio
            if i != 0 or palabra in ['Maria', 'Juan', 'Pedro', 'Madrid','Perez','Barcelona']:
                candidatos.append(palabra)
# Contar ocurrencias
conteo = Counter(candidatos)

# Mostrar resultados
print("Texto original:", texto)
print("Nombres propios detectados:", list(conteo.keys()))
print("Frecuencia:", conteo)
