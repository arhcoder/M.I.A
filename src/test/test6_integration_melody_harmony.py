import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



print("\nMIA INTEGRATION OF MELODY AND HARMONY\n")



#/ INTEGRATION ---------------------------------------------------------------------- #/
print(f"{'* Importing engines':<40}", end="")
from Blocks.Melody import Melody
from Blocks.Harmony import Harmony
from Blocks.Chord import Chord

from Rythm import Rythm
from Progressions import GeneticProgression

from conf import simulated_annealing_phrases_params
from conf import genetic_progression_params
print("✅")



#/ SONG PARAMETERS -------------------------------------------------------------------- #/
key = "C"
scale = "major"
signature = (4, 4)
bars_per_sentence = 1
upbeat = 1
chords_octave = 2



#/ MELODY GENERATION -----------------------------------------------------------------. /#
print("\nMELODY GENERATION")

#? LIST OF SENTENCES:
print(f"{'* Generating sentences':<40}", end="")
sentence1s = "Hey jude"
sentence1 = ["hey*", " ", "jude*"]
chords_for_s1 = 1

sentence2s = "Don't make it bad"
sentence2 = ["dont*", " ", "make'*", " ", "it'*", " ", "bad*"]
chords_for_s2 = 1

sentence3s = "Take a sad song"
sentence3 = ["take*'", " ", "a*", "sad*", " ", "song*"]
chords_for_s3 = 1

sentence4s = "And make it better"
sentence4 = ["and*", " ", "make'*", " ", "it*", " ", "be*", "tte", "e", "er*"]
chords_for_s4 = 1

sentences = [
    (sentence1s, sentence1),
    (sentence2s, sentence2),
    (sentence3s, sentence3),
    (sentence4s, sentence4)
]
print("✅")

#? RYTHM GENERATION:
#* Rythm object to fit all sentences:
print(f"{'* Generating Ryths':<40}", end="")
rythm_melody = Rythm(
    signature=signature,
    upbeat=upbeat,
    params=simulated_annealing_phrases_params
)
print("✅")

#* Melody object to append the rythmic phrases:
print(f"{'* Fitting sentences into rythm phrases':<40}", end="")
melody = Melody(
    signature=signature,
    key_name=key,
    key_type=scale,
    upbeat=upbeat
)
#* Fit method for each sentence:
for i, (sentence_str, sentence_tokens) in enumerate(sentences):
    phrase = rythm_melody.fit(
        sentence=sentence_tokens,
        bars=bars_per_sentence
    )
    #* Adding the result Phrase objecto to melody:
    melody.add_element(phrase)
print("✅")



#/ CHORDS GENERATION ------------------------------------------------------------------ /#
print("\nCHORDS PROGRESSION GENERATION")

#? SIMPLE CHORDS GENERATION:
#* Amount of chords:
amount_of_chords_list = [chords_for_s1, chords_for_s2, chords_for_s3, chords_for_s4]

#* Class GeneticProgression to get simple chord progression:
print(f"{'* Creating Genetis':<40}", end="")
progressions = GeneticProgression(
    params=genetic_progression_params
)
print("✅")

#* Creating n amount of chords for progression:
n_chords = sum(amount_of_chords_list)

#* Returns as list[tuple] in which each tuple has:
#*  - [str] Name of root note on the chord
#*  - [str] Type of the chord
#*  - [str] Degree of the chord on the key
#*  - [int] Inversion (if 0, it is fundamental state)
print(f"{'* Generating Progressios':<40}", end="")
progressions = progressions.create(
    chords=n_chords,
    key=key,
    scale=scale
)
print("✅")

#* Gives rythm to the chords:
print(f"{'* Generating Ryths':<40}", end="")
rythm_harmony = Rythm(
    signature=signature,
    upbeat=upbeat,
    params=simulated_annealing_phrases_params,
    for_chords=True
)
print("✅")

#* For each phrase it gets the amount of chords and gets the rythm:
print(f"{'* Fitting chords into ryths':<40}", end="")
chords_durations = []
chords_dots = []
for chord in amount_of_chords_list:
    chord_sentence = ["X*"] * chord
    # times_chords = (initial_rest, syllable_figures, final_rest, dots)
    times_chords = rythm_harmony.fit(
        sentence=chord_sentence,
        bars=bars_per_sentence
    )
    chords_durations.extend(times_chords[1])
    chords_dots.extend(times_chords[3][1:-1])
if len(progressions) == len(chords_durations) == len(chords_dots):
    print("✅")
else:
    print("❌ Sizes of chords do not match:")
    print("    - Chords Progression size:", len(progressions))
    print("    - Chords Time Durations size:", len(chords_durations))
    print("    - Chords Durations dots size:", len(chords_dots))

#* Construct each chord into the harmony: 
print(f"{'* Ensambling chords':<40}", end="")
harmony = Harmony(
    signature=signature,
    key_name=key,
    key_type=scale,
    upbeat=upbeat
)
for i in range(len(progressions)):
    chord = Chord(
        name=progressions[i][0],
        ctype=progressions[i][1],
        inversion=progressions[i][3],
        octave=chords_octave,
        time=chords_durations[i],
        dot=chords_dots[i]
    )
    harmony.add_element(chord)
print("✅")



#! FINAL RESULTS -----------------------------------------------------------------------!#
print("\nGENERATED MUSICAL IDEA\n")

#? MELODY:
print("═"*40)
print("MELODY")
print("═"*40)
print(melody)
print("═"*40)

print()

#? HARMONY:
print("═"*40)
print("HARMONY")
print("═"*40)
print(harmony)
print("═"*40)

print()

#! -------------------------------------------------------------------------------------!#