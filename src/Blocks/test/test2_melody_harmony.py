from Note import Note
from Phrase import Phrase
from Chord import Chord

from Melody import Melody
from Harmony import Harmony


#! TESTING MELODY AND HARMONY !#


#/ MELODY:
#* EXAMPLE OF "Aria di Mezzo Carattere":
melody = Melody(signature=(4, 4), key_name="D", key_type=1, upbeat=1)

#? Phrases:
phrase1 = Phrase()
note1 = Note(time=8, note="F#", octave=5, dot=False)
note2 = Note(time=8, note="G", octave=5, dot=False)
note3 = Note(time=4, note="A", octave=5, dot=False)
note4 = Note(time=2, note="D", octave=4, dot=False)
phrase1.add_end(note1)
phrase1.add_end(note2)
phrase1.add_end(note3)
phrase1.add_end(note4)

phrase2 = Phrase()
note5 = Note(time=8, note="F#", octave=5, dot=False)
note6 = Note(time=8, note="G#", octave=5, dot=False)
note7 = Note(time=4, note="A", octave=5, dot=False)
note8 = Note(time=2, note="C#", octave=6, dot=False)
phrase2.add_end(note5)
phrase2.add_end(note6)
phrase2.add_end(note7)
phrase2.add_end(note8)

melody.add_element(phrase1)
melody.add_element(phrase2)


#/ HARMONY:
harmony = Harmony(signature=(4, 4), key_name="D", key_type=1, upbeat=1)

chord1 = Chord(name="D", ctype="", inversion=0, octave=3, time=1, dot=False)
chord2 = Chord(name="F#", ctype="m", inversion=0, octave=3, time=1, dot=False)

harmony.add_element(chord1)
harmony.add_element(chord2)

# Print the staffs:
print("\nARIA DI MEZZO CARATTERE")
print(melody)
print()
print(harmony)