import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Key import notes_of_scale, chords_of_scale


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