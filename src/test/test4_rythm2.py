import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Rythm import Rythm
from conf import simulated_annealing_phrases_params

# Sentences in eglish:
sentence1s = "Hey jude"
sentence1 = ["hey*", " ", "jude*"]

sentence2s = "Don't make it bad"
sentence2 = ["dont*", " ", "make'*", " ", "it'*", " ", "bad*"]

sentence3s = "Take a sad song"
sentence3 = ["take*'", " ", "a*", "sad*", " ", "song*"]

sentence4s = "And make it better"
sentence4 = ["and*", " ", "make'*", " ", "it*", " ", "be*", "tte*", "e*", "er*"]

sentences = [
    (sentence1s, sentence1),
    (sentence2s, sentence2),
    (sentence3s, sentence3),
    (sentence4s, sentence4)
]
signature = (4, 4)
bars_per_sentence = 1
upbeat = 1

rythm_instance = Rythm(signature=signature, upbeat=upbeat, params=simulated_annealing_phrases_params)
for i, (sentence_str, sentence_tokens) in enumerate(sentences):

    phrase = rythm_instance.fit(sentence_tokens, bars=bars_per_sentence)
    print(f"\nSentence {i+1}:")
    print(f"\n * {sentence_str}\n")
    print(phrase)