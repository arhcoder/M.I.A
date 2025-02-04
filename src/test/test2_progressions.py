import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Progressions import GeneticProgression

progressions = GeneticProgression()
progressions.create(4, "C", "major")