
#! PARAMETERS TO MODIFY IN WAY TO SET THE ALGORITHMS RESULTS !#

#? [01] CHORD PROGRESSIONS:
genetic_progression_params = {
    "population_size": 50,
    "generations": 50,
    "mutation_rate": 0.1,
    "tournament_size": 5,
    "elitism_size": 3,

    #? FOR INITIALIZATION:
    #* In the step to initializate, the complexity is how complex the chords will be:
    #* If complexity = 0, it just will take basics major - minor (sometimes dim)
    #* If complexity = 100, it will take with some frequency complex chords as maj11, m7b5, 7#5, etc
    #/ SO, if complexity is up to 50, the chords must be more jazzy,
    #! But if the mutation rate is near to 1 (100%), then will be more possible to see rare chords,
    #! but unestable chord progressions;
    #? It has to be between 0 and 100:
    "chords_complexity": 20,

    "scoring_prefs": {
        "first_chord_is_tonic": 4,
        "first_chord_not_tonic_penalty": 0,
        "last_chord_is_dominant": 4,
        "last_chord_not_dominant_penalty": 0,
        "first_last_combined_bonus": 10,
        "tonic_on_last_bonus": 5,
        "dominant_precedes": 20,
        "cadence": 30,
        "scale_membership_multiplier": 20,
        "diversity_multiplier": 30,
        "voice_leading_multiplier": 10,
        "sus_before_major": 4,
        "complexity_penalty_factor": 30,
        "dominant_seventh_bonus": 15,
        "tension_resolution": 10
    }
}