import random
from Key import chords_of_scale, degree_of_chord, diatonics
from Selectors import lwrs, cwrs
from Data.harmony.chords import patterns, classifications
from conf import genetic_progression_params


class GeneticProgression:

    def __init__(self):

        # Load GA parameters from config file:
        self.params = genetic_progression_params
        self.notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.population = []
    
    
    #? MAIN FUNCTION TO CREATE A PROGRESSION:
    def create(self, chords: int, key: str, scale: str):
        """
            Main method to get a progression acoording to a key, with Genetic Algorithm

            Parameters:
                - chords [int]: Amount of chords on the progression
                - key [str]: Name of the key
                    It could be some of this values:
                    ["C", "D", "E", "F", "G", "A", "B"]
                    Or some of this values:
                    ["C#", "D#", "F#", "G#", "A#"] or ["Db", "Eb", "Gb", "Ab", "Bb"]
                - scale [str]: Name of the type of scale
                    Only diatonic scales supported:
                    - "major"
                    - "minor"
                    - "minor harmonic"
                    - "minor melodic"
                    - "ionian"
                    - "dorian"
                    - "phrygian"
                    - "lydian"
                    - "mixolydian"
                    - "aeolian"
                    - "locrian"

            Returns: Best solution of chord progression in format:
                list[tuple] in which each tuple has:
                    - [str] Name of root note on the chord
                    - [str] Type of the chord
                    - [str] Degree of the chord on the key
                    - [int] Inversion (if 0, it is fundamental state)
                    Example of progression:
                    [
                        ("C", "", "I", 0): C major as I degree on fundamental state: C-E-G
                        ("A", "m", iv, 0): A minor as iv degree on fundamental state: A-C-E
                        ("F", "", VI, 1): F major as VI degree on first inversion: A-C-F
                        ("G", "7", V, 2): G major with minor 7th on second inversion: D-F-G-B
                    ]
        """
        #? Some validations:
        if not isinstance(chords, int) or chords < 2:
            raise ValueError("\"chords\" must be integer higher than 1")
        
        flats_to_sharps = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
        key = key.capitalize()
        if not key in flats_to_sharps.keys() and not key in self.notes:
            raise ValueError(f"\"key\" must be any from {self.notes + list(flats_to_sharps.keys())}")
        
        scale = scale.lower()
        if not scale in diatonics.keys():
            raise ValueError(f"\"scale\" must be any from {list(diatonics.keys())}")

        #? Flats to sharp:
        if key in flats_to_sharps:
            key = flats_to_sharps[key]
        
        #/ GENETIC ALGORITHM /#
        #? Initializate population:
        self.population = self.initialize(self.params["population_size"], chords, key, scale)


        #! STOP BEFORE THE IMPLEMENTATION OF OBJECTIVE FUNCTION, TO TEST POPULATION INITIALIZATION:
        print(f"GENETIC ALGORITHM PROGRESSIONS\nIn key of {key} {scale}:")
        for i, progression in enumerate(self.population):
            print(f"\nProgression {i+1}:")
            for chord in progression:
                print(f" * {chord[0]}{chord[1]}\t\t[{chord[2]}]\t\t{chord[3]}")
        return

        #? Generaton steps: 
        for _ in range(self.params["generations"]):

            #? Evaluation of progressions:
            evaluated = [(self.rate(ind), ind) for ind in self.population]
            evaluated.sort(reverse=True, key=lambda x: x[0])
            
            #? Elitism: keep top solutions:
            elite = [ind for (_, ind) in evaluated[:self.params["elitism_size"]]]
            
            #? New self.population:
            children = []
            while len(children) < self.params["population_size"] - self.params["elitism_size"]:
                parent1 = self.selection(self.population)
                parent2 = self.selection(self.population)
                child1, child2 = self.crossover(parent1, parent2)
                children.append(self.mutate(child1, key, scale))
                children.append(self.mutate(child2, key, scale))
            self.population = elite + children[:self.params["population_size"] - self.params["elitism_size"]]
        
        return max(self.population, key=lambda x: self.rate(x))
    

    #? Initialization with LWRS:
    def initialize(self, size: int, chords: int, key: str, scale: str):

        #* Step 1: Get chords_in the key/scale (ignore degree):
        scale_chords = chords_of_scale(key, scale)
        chords_in = [(root, ctype) for root, ctype, _ in scale_chords]

        #* Step 2: Generate chords_out (maj/min not in chords_in):
        chords_out = []
        for note in self.notes:

            # Check if major chord is in scale:
            if (note, "") not in chords_in:
                chords_out.append((note, ""))

            # Check if minor chord is in scale:
            if (note, "m") not in chords_in:
                chords_out.append((note, "m"))

        #* Step 3: Prepare in/out selection list for lwrs algorithm:
        in_out_list = ["in"] * 7 + ["out"] * 5

        #* Step 4: Generation of population:
        population = []
        for _ in range(size):

            progression = []
            for _ in range(chords):

                #* Step 5: Selection of the chord in basic mode (just major or minor or dim or aug)
                #? It uses Logarithmic Random Weighted Selector (lwrs) to select if the chord is on the key or not:
                selection = lwrs(in_out_list)
                if selection == "in":
                    root, ctype = random.choice(chords_in)
                else:
                    root, ctype = random.choice(chords_out)

                #* Step 6: Selects the chord complexity based on the parameter "chords_complexity";
                #* It Apply chord complexity modifications to major/minor or augmented/diminished chords:
                #? It takes the complexity, with the algorithm Complexity Weighted Random Selector (cwrs);
                #? This method gives probability of chord complexity according to:
                #?  1. If complexity is 0, the the 100% times it will keep just major/minor (or aumented/diminished)
                #?      chords (first element on the list has 100%)
                #?  2. If complexity is up to 50, then the first element (just major/minor) (or aumented/diminished)
                #?      has the 50% to appear, the rest of chords has more probability
                #?  3. If complexity is 100, then all the chord types has the same probabiility to be selected
                #/ If complexity is near to 100, the chords will be more jazzy, if near to 0, more simle chords

                # First get the category (major/minor) (aumented/diminished):
                category = classifications[ctype]
                same_category = [t for t in classifications if classifications[t] == category]

                # Select new chord type based on complexitty:
                ctype = cwrs(same_category, self.params["chords_complexity"])

                #* Step 7: Determine degree:
                degree = degree_of_chord(root, ctype, key, scale)

                #* Step 9: Select inversion:
                inversion = lwrs([*range(0, len(patterns[ctype]))])

                #* Step 10: Build chord tuple and add to progression:
                chord_tuple = (root, ctype, degree, inversion)
                progression.append(chord_tuple)

            population.append(progression)

        return population
    

    #? Tournament selection:
    def selection(self):
        contestants = random.sample(self.population, self.params["tournament_size"])
        return max(contestants, key=lambda x: self.rate(x))
    
    
    #? Single point crossover:
    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1)-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    

    #? Replace completly some random chord on the progression:
    def mutate(self, solution, key, scale):
        if random.random() < self.params["mutation_rate"]:
            idx = random.randint(0, len(solution)-1)
            new_root = random.choice(self.notes)
            new_type = random.choice(list(patterns.keys()))
            new_degree = degree_of_chord(new_root, new_type, key, scale)
            new_inversion = random.choice([*range(0, len(patterns[new_type]))])
            solution = solution[:idx] + [(new_root, new_type, new_degree, new_inversion)] + solution[idx+1:]
        return solution
    



    #/ OBJECTIVE FUNCTION /#
    #* THE LOGIC TO GET BETTER CHORDS *#
    def rate(self, progression):
        pass