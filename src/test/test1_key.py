import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from Key import notes_of_scale, chords_of_scale, degree_of_chord
#! TEST CASES:
test_cases = [
    ("C", "Ionian"),
    ("D", "Dorian"),
    ("E", "Phrygian"),
    ("F", "Lydian"),
    ("G", "Mixolydian"),
    ("A", "Aeolian"),
    ("B", "Locrian"),
    ("A", "Minor Harmonic"),
    ("A", "Minor Melodic")
]


#! TESTING GET NOTES OF SCALE:
for root, scale in test_cases:
    print(f"\nNotes of {root} {scale}:")
    notes = notes_of_scale(root, scale)
    print(f" * {', '.join(notes)}")
print()


#! TESTING GET CHORDS OF SCALE:
for key, scale in test_cases:
    print(f"\nChords for {key} {scale}:")
    chords = chords_of_scale(key, scale)
    #? Chord format example: ("G", "m", "v")
    for chord in chords:
        print(f" * {chord[2]}: {chord[0]}{chord[1]}")
print()


#! TESTING DEGREE_OF_CHORD:
print("\nChords degree on C Major context:")
test_chords = [
    ("C", ""),
    ("D", "m"),
    ("E", "m"),
    ("F", ""),
    ("G", "7"),
    ("A", "m"),
    ("B", "dim"),
    ("C#", "m"),
    ("Eb", "m"),
    ("F#", "aug"),
    ("G", "m7"),
    ("G", "dim"),
    ("C", "maj7"),
    ("D", "7"),
    ("G#", "aug"),
    ("A", "m7b5")
]
for root, ctype in test_chords:
    try:
        degree = degree_of_chord(root, ctype, "C", "Major")
        print(f" * {root}{ctype}: {degree}")
    except ValueError as e:
        print(f" * {root}{ctype}: ERROR: {str(e)}")
print()