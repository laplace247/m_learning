from nltk.tokenize import TreebankWordTokenizer

# Listas simples (se pueden ampliar)

positivas = {'bueno', 'excelente', 'positivo', 'feliz', 'genial'}
negativas = {'malo', 'terrible', 'negativo', 'horrible', 'triste'}

texto = "El producto es excelente y me hace muy feliz, pero el servicio fue terrible."

tokenizer = TreebankWordTokenizer()
tokens = tokenizer.tokenize(texto)

#Contar sentimientos
positivo = sum(1 for palabra in tokens if palabra.lower() in positivas)
negativo = sum(1 for palabra in tokens if palabra.lower() in negativas)

print(f"Conteo de palabras positivas: {positivo}")
print(f"Conteo de palabras negativas: {negativo}")

if positivo > negativo:
    print("El sentimiento general: POSITIVO")
elif negativo > positivo:
    print("El sentimiento general: NEGATIVO")
else:
    print("El sentimiento general: NEUTRO")
