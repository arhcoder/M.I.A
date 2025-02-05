import pandas as pd
import random

# Takes the circle of fifths:
Circle = pd.read_csv("circle-of-fifths.csv").to_numpy()

# Selects a random tonality:
tonality = random.randint(0, 11)

# Selects a random of major or minor tonality:
# if minor = 1: minor; if minor = 0: major;
minor = random.randint(0, 1)

# Select the chords of the tonality:
chords = [("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", ""), ("", "")]
# It takes the fifths circle and take the neighbors of the tonality:
# CIRCLE OF FIFTHS:
#* C   G   D   A   E   B   F#  C#  G#  D#  A#  F;
#* Am  Em  Bm  Fm# C#m G#m D#m A#m Fm  Cm  Gm  Dm;
#? If the tonality is "G#", the chords on the scale are the neighbors;
#? in this case C#, D#, A#m Fm Cm;
#? The dismished chord is taked for the second line, the next chord to
#? the last neighbor; in this case is Fm (Fdismished);

#/ When the scale is major (G# for example):
#*  The first grade is: MAJOR; TONALITY (G#);
#*  The second grade is: MINOR; TONALITY - 1 (D#m);
#*  The third grade is: MINOR; TONALITY + 1 (Cm);
#*  The fourth grade is: MAJOR; TONALITY - 1 (C#);
#*  The fifth grade is: MAJOR; TONALITY + 1 (D#);
#*  The sixth grade is: MINOR; TONALITY (Fm);
#*  The seventh grade is: (MINOR); TONALITY + 2 DIM (Gdim);

#/ When the scale is minor (F#m for example):
#*  The first grade is: MINOR; TONALITY (F#m);
#*  The second grade is: (MINOR); TONALITY + 2 Dim (G#dim);
#*  The third grade is: MAJOR; TONALITY (A);
#*  The fourth grade is: MINOR; TONALITY - 1 (Bm);
#*  The fifth grade is: MINOR; TONALITY + 1 (C#m);
#*  The sixth grade is: MAJOR; TONALITY - 1 (D);
#*  The seventh grade is: MAJOR; TONALITY + 1 (E);

print(f"\nFor {Circle[minor][tonality]:} key;\nChords:\n")

#/ It uses index to identify the neighbors of a chord:
#/ It is a weird and fool way to interpret it, but only
#/ fot the moment it will be int this way:
plus2Index = tonality + 2
plus1Index = tonality + 1
less1Index = tonality - 1

#/ For the special cases when the chord is on the
#/ extrems of the chords list:
# When it is the first index:
if tonality == 0:
    less1Index = 11
# When it is the second index:
# When it is the last index:
elif tonality == 11:
    plus2Index = 1
    plus1Index = 0
# When it is the penultimate index:
elif tonality == 10:
    plus2Index = 0

# To identify the non-selected major-minor tonality:
# anotherMinor = 0 if minor == 1 else 1

#? Gets the respective chords of the tonality:
#/ For majors:
if minor == 0:

    #* The first grade is: MAJOR; TONALITY;
    chords[0] = ("I", Circle[minor][tonality])

    #* The second grade is: MINOR; TONALITY - 1;
    chords[1] = ("ii", Circle[1][less1Index])

    #* The third grade is: MINOR; TONALITY + 1;
    chords[2] = ("iii", Circle[1][plus1Index])

    #* The fourth grade is: MAJOR; TONALITY - 1;
    chords[3] = ("IV", Circle[0][less1Index])

    #* The fifth grade is: MAJOR; TONALITY + 1;
    chords[4] = ("V", Circle[0][plus1Index])

    #* The sixth grade is: MINOR; TONALITY;
    chords[5] = ("iv", Circle[1][tonality])

    #* The seventh grade is: (MINOR); TONALITY + 2 DIM;
    chords[6] = ("vii", Circle[1][plus2Index][0]+"dim")

#/ For minors:
else:

    #* The first grade is: MINOR; TONALITY;
    chords[0] = ("i", Circle[minor][tonality])

    #* The second grade is: (MINOR); TONALITY + 2 Dim;
    chords[1] = ("ii", Circle[1][plus2Index][0]+"dim")

    #* The third grade is: MAJOR; TONALITY;
    chords[2] = ("III", Circle[0][tonality])

    #* The fourth grade is: MINOR; TONALITY - 1;
    chords[3] = ("iv", Circle[1][less1Index])

    #* The fifth grade is: MINOR; TONALITY + 1;
    chords[4] = ("v", Circle[1][plus1Index])

    #* The sixth grade is: MAJOR; TONALITY - 1;
    chords[5] = ("VI", Circle[0][less1Index])

    #* The seventh grade is: MAJOR; TONALITY + 1;
    chords[6] = ("VII", Circle[0][plus1Index])

#! Shows the respective chords of the tonality:
for i in range(0, 7):
    print(f"{chords[i][0]}°:\t{chords[i][1]}")

print()

'''
    It is maybe a useless script, because I don't really
    know which will be the exactly representation of chords,
    scales, notes, etc. I'm not sure if it is the best option
    to "calculate" the chords of a tonality, or only take it
    from a complete table.

    I'm not sure how I will incorporate another scales mode
    chords, and if it will be a good idea.

    It is only a util, whit not the best optimization.
    Greetings!
'''