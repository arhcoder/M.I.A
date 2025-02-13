import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Rythm import Rythm
from conf import simulated_annealing_phrases_params

# Sentences in spanish:
sentence1s = "Voz de la guitarra mía"
sentence1 = ["voz*", " ", "de*", " ", "la*", " ", "gui*", "ta", "rra", " ", "mí*", "a"]

sentence2s = "Al despertar la mañana"
sentence2 = ["al*", " ", "des", "per", "tar*", " ", "la*", " ", "ma", "ña*", "na"]

sentence3s = "Viene a cantar su alegría"
sentence3 = ["vie*", "ne", " ", "a", " ", "can", "tar*", " ", "su*", " ", "a", "le", "grí*", "a"]

sentence4s = "A mi tierra mexicana"
sentence4 = ["a*", " ", "mi*", " ", "tie", "rra*", " ", "me", "xi", "ca*", "na"]

sentences = [
    (sentence1s, sentence1),
    (sentence2s, sentence2),
    (sentence3s, sentence3),
    (sentence4s, sentence4)
]
signature = (3, 4)
bars_per_sentence = 4
upbeat = 0

rythm_instance = Rythm(signature=signature, upbeat=upbeat, params=simulated_annealing_phrases_params)
for i, (sentence_str, sentence_tokens) in enumerate(sentences):

    phrase = rythm_instance.fit(sentence_tokens, bars=bars_per_sentence)
    print(f"\nSentence {i+1}:")
    print(f"\n * {sentence_str}\n")
    print(phrase)