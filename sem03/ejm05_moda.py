from nltk.tokenize import TreebankWordTokenizer
from nltk.corpus import stopwords
from collections import Counter
import nltk

nltk.data.path.append('C:\\Users\\Estudiante\\Downloads\\nltk_data')

texto = "Hola, espero que bien si estás bien me alegro mucho."

tokenizer = TreebankWordTokenizer()
tokens = tokenizer.tokenize(texto.lower())

stop_words = set(stopwords.words('spanish'))

tokens_filtrados = [i for i in tokens if i not in stop_words]
conteo=Counter(tokens_filtrados)

print('Conteo de palabras:')
for palabra, frecuencia in conteo.items():
    print(f'{palabra}: {frecuencia}')

