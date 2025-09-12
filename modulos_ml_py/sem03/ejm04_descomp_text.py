#pip install nltk==3.8.1
from nltk.tokenize import TreebankWordTokenizer

tokenizer = TreebankWordTokenizer()
texto = "Hola, ¿cómo estás? Espero que bien. ¡Nos vemos pronto!"
tokens = tokenizer.tokenize(texto)

print("Tokens:", tokens)