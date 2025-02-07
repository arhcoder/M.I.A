import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Rythm import Rythm
from Data.rythm.times import TIMES

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

rythm_instance = Rythm(signature=signature, upbeat=upbeat)
for i, (sentence_str, sentence_tokens) in enumerate(sentences):

    initial_rest, syllable_figures, final_rest, dots = rythm_instance.fit(sentence_tokens, bars=bars_per_sentence)
    processed_syllables = rythm_instance.preprocess_syllables(sentence_tokens)
    
    full_notes = [initial_rest] + syllable_figures + [final_rest]
    full_syllables = ["(rest)"] + processed_syllables + ["(rest)"]
    full_dots = dots

    print(f"\nSentence {i+1}:")
    print(f"\n * {sentence_str}")
    print()
    for j in range(len(full_notes)):
        note_val = full_notes[j]
        dot_flag = full_dots[j]
        label = full_syllables[j]
        note_id_str = f"{note_val}•" if dot_flag else f"{note_val}"
        note_name_str = f"{TIMES.get(note_val, 'x')[0]}•" if dot_flag else TIMES.get(note_val, 'x')[0]
        print(f"    - {label}\t{note_id_str}\t{note_name_str}")