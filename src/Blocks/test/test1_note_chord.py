from Blocks.Note import Note
from Blocks.Chord import Chord


#! TESTING NOTES AND CHORDS !#


#/ TESTING NOTES:
note1 = Note(4, "A", 4)
print(note1)
note1.note = "B"
print(note1)
note1.octave = 6
print(note1)
note1.dot = True
print(note1)
note1.time = 2
print(note1)
note1.tuning = 432
print(note1)

note2 = Note(3, "C#", 5)
note3 = Note(12, "E", 6)
note4 = Note(1, "Bb", 6, dot=True)
note5 = Note(8, "A#", 6)
note6 = Note(3, "X", 4)
print(note2)
print(note3)
print()
print(note4)
print(note5)
print(note6)

# note7 = Note(0, "C", 6)
# print(note7)

# note8 = Note(5, "A#", 6)
# print(note8)

# note9 = Note(6, "C", 4.5)
# print(note9)


#/ TESTING CHORDS:
chord1 = Chord(name="C", ctype="", inversion=0, octave=4, time=4)
chord2 = Chord(name="C", ctype="", inversion=1, octave=4, time=4)
chord3 = Chord(name="C", ctype="", inversion=2, octave=4, time=4)
chord4 = Chord(name="C", ctype="", inversion=3, octave=4, time=4)

chord5 = Chord(name="C", ctype="maj7", inversion=0, octave=4, time=4)
chord6 = Chord(name="C", ctype="maj7", inversion=1, octave=4, time=4)
chord7 = Chord(name="C", ctype="maj7", inversion=2, octave=4, time=4)
chord8 = Chord(name="C", ctype="maj7", inversion=3, octave=4, time=4)
chord9 = Chord(name="C", ctype="maj7", inversion=0, octave=5, time=4)

chord10 = Chord(name="F#", ctype="7", inversion=0, octave=2, time=4)
chord11 = Chord(name="Bb", ctype="m7", inversion=0, octave=3, time=4)
chord12 = Chord(name="B", ctype="sus2", inversion=0, octave=3, time=4)
chord13 = Chord(name="Ab", ctype="dim", inversion=3, octave=1, time=4)

chord14 = Chord(name="X", ctype="", inversion=0, octave=1, time=4)

print(chord1, end="\n\n")
print(chord2, end="\n\n")
print(chord3, end="\n\n")
print(chord4, end="\n\n")
print(chord5, end="\n\n")
print(chord6, end="\n\n")
print(chord7, end="\n\n")
print(chord8, end="\n\n")
print(chord9, end="\n\n")
print(chord10, end="\n\n")
print(chord11, end="\n\n")
print(chord12, end="\n\n")
print(chord13, end="\n\n")
print(chord14, end="\n\n")

print("\nCHORDS CHANGES: -------------------------------------")
chord16 = Chord(name="C", ctype="", inversion=0, octave=4, time=4)
print(chord16, end="\n\n")
chord16.name = "F"
print(chord16, end="\n\n")
chord16.ctype = "m"
print(chord16, end="\n\n")
chord16.inversion = 2
print(chord16, end="\n\n")
chord16.octave = 2
print(chord16, end="\n\n")
chord16.time = 1
print(chord16, end="\n\n")
chord16.dot = True
print(chord16, end="\n\n")
chord16.tuning = 432
print(chord16, end="\n\n")
chord16.name = "X"
chord16.tuning = 440
print(chord16, end="\n\n")