
#! PARAMETERS TO MODIFY IN WAY TO SET THE ALGORITHMS RESULTS !#

#? [01] CHORD PROGRESSIONS:
genetic_progression_params = {
    "population_size": 100,
    "generations": 60,
    "mutation_rate": 0.2,
    "tournament_size": 3,
    "elitism_size": 5,

    #? FOR INITIALIZATION:
    #* In the step to initializate, the complexity is how complex the chords will be:
    #* If complexity = 0, it just will take basics major - minor (sometimes dim)
    #* If complexity = 100, it will take with some frequency complex chords as maj11, m7b5, 7#5, etc
    #/ SO, if complexity is up to 50, the chords must be more jazzy,
    #! But if the mutation rate is near to 1 (100%), then will be more possible to see rare chords,
    #! but unestable chord progressions;
    #? It has to be between 0 and 100:
    "chords_complexity": 40
}