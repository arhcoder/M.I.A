from Note import Note

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