from words import complete_sentence

categories = "Det Sus Adj VConj Det Sus"
oracion = complete_sentence(categories)

palabras = [palabra["word"] for palabra in oracion]
silabas = [palabra["syllables"] for palabra in oracion]
tonicas = [palabra["tonic"] for palabra in oracion]

print(f"Input: {categories}")
print(f"Oración generada: {' '.join(palabras)}")
print(f"Sílabas: {silabas}")
print(f"Tónicas: {tonicas}")