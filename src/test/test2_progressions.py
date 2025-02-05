import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Progressions import GeneticProgression

key = "C"
scale = "major"
progressions = GeneticProgression()
best_progression = progressions.create(8, key, scale)
population = progressions.all()

print(f"GENETIC ALGORITHM PROGRESSIONS\nIn key of {key} {scale}:")
for i, (score, progression) in enumerate(population):
    print(f"\nProgression {i+1} (Score: {score:.2f}):")
    for chord in progression:
        chord_symbol = f"{chord[0]}{chord[1]}" if chord[1] else chord[0]
        print(f"  - {chord_symbol:<6} {chord[2]}\tInversion: {chord[3]}")


print("\n\nBEST PROGRESSION:")
print("|\t" + "\t".join([f"{chord[0]}{chord[1]}" for chord in best_progression]) + "\t|")
print("|\t" + "\t".join([chord[2] for chord in best_progression]) + "\t|")
print("|\t" + "\t".join([str(chord[3]) for chord in best_progression]) + "\t|")
print()