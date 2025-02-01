
#? CONSTANTS:

from Data.harmony.chords import patterns
diatonics = {
    
    "major": ([0, 2, 4, 5, 7, 9, 11], "major"),
    "minor": ([0, 2, 3, 5, 7, 8, 10], "minor"),

    "minor harmonic": ([0, 2, 3, 5, 7, 8, 11], "minor"),
    "minor melodic": ([0, 2, 3, 5, 7, 9, 11], "minor"),

    "ionian": ([0, 2, 4, 5, 7, 9, 11], "major"),
    "dorian": ([0, 2, 3, 5, 7, 9, 10], "minor"),
    "phrygian": ([0, 1, 3, 5, 7, 8, 10], "minor"),
    "lydian": ([0, 2, 4, 6, 7, 9, 11], "major"),
    "mixolydian": ([0, 2, 4, 5, 7, 9, 10], "major"),
    "aeolian": ([0, 2, 3, 5, 7, 8, 10], "minor"),
    "locrian": ([0, 1, 3, 5, 6, 8, 10], "minor")
}
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


#? METHODS:
def notes_of_scale(root: str, scale: str):
    """
        Gets the list of notes of a scale

        Parameter:
            - root [str]: Name of the root note
                It could be some of this values:
                ["C", "D", "E", "F", "G", "A", "B"]
                Or some of this values:
                ["C#", "D#", "F#", "G#", "A#"] or ["Db", "Eb", "Gb", "Ab", "Bb"]
            - scale [str]: Name of the scale
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
        Returns:
            - [list] of strings of the notes
            NOTE: name of the note always with just sharps (#) no flats (b) notation
    """
    # Capitalize and lower case of parameters:
    root = root.capitalize()
    scale = scale.lower()

    # Flats to sharp:
    flats_to_sharps = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
    if root in flats_to_sharps:
        root = flats_to_sharps[root]
    
    # Validate scale name:
    if scale not in diatonics:
        raise ValueError(f"Scale \"{scale}\" not supported.\nAvailable scales: {list(diatonics.keys())}")

    # Interval patterns:
    scale_pattern, _ = diatonics[scale]
    try:
        root_index = note_names.index(root)
    except ValueError:
        raise ValueError(f"Root note \"{root}\" not valid. Use one of {note_names}")
    
    # Returns the list of patterns:
    return [note_names[(root_index + interval) % 12] for interval in scale_pattern]


def chords_of_scale(key: str, scale: str):
    """
        Gets the list of chords from a key/scale

        Parameter:
            - key [str]: Name of the key/scale
                It could be some of this values:
                ["C", "D", "E", "F", "G", "A", "B"]
                Or some of this values:
                ["C#", "D#", "F#", "G#", "A#"] or ["Db", "Eb", "Gb", "Ab", "Bb"]
            - scale [str]: Name of type of scale
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
        Returns:
            - [list[tuple]] where tuple has: (name of the chord, type of the chord, grades grade)
              NOTE: name of the note always with just sharps (#) no flats (b) notation
    """
    # Process key to handle capitalization and flats:
    # Flats to sharp:
    flats_to_sharps = {"Db": "C#", "Eb": "D#", "Gb": "F#", "Ab": "G#", "Bb": "A#"}
    if key in flats_to_sharps:
        key = flats_to_sharps[key].capitalize()
    
    # Process scale to lower case:
    scale = scale.lower()
    if scale not in diatonics:
        raise ValueError(f"Scale \"{scale}\" not supported.\nAvailable scales: {list(diatonics.keys())}")
    intervals, _ = diatonics[scale]
    
    # Generate scale notes:
    try:
        key_index = note_names.index(key)
    except ValueError:
        raise ValueError(f"Invalid key: {key}")
    scale_notes = [note_names[(key_index + interval) % 12] for interval in intervals]
    
    # Generate major scale notes for accidentals comparison:
    major_scale_intervals = diatonics["major"][0]
    major_scale_notes = [note_names[(key_index + interval) % 12] for interval in major_scale_intervals]
    
    # Prepare Roman numerals:
    grades = ["I", "II", "III", "IV", "V", "VI", "VII"]
    chords = []
    
    # Mapping from pattern names to chord types:
    # Change if can cahnge the format of chord type #
    triad_type_mapping = {
        "": "",
        "m": "m",
        "dim": "dim",
        "aug": "aug",
        "sus2": "sus2",
        "sus4": "sus4"
    }
    
    for i in range(7):
        root = scale_notes[i]
        third_note = scale_notes[(i + 2) % 7]
        fifth_note = scale_notes[(i + 4) % 7]
        
        root_idx = note_names.index(root)
        third_idx = note_names.index(third_note)
        fifth_idx = note_names.index(fifth_note)
        
        third_semitones = (third_idx - root_idx) % 12
        fifth_semitones = (fifth_idx - root_idx) % 12
        
        triad_intervals = sorted([0, third_semitones, fifth_semitones])
        chord_pattern = None
        
        # Find the matching triad pattern:
        for pattern_name, pattern in patterns.items():
            if len(pattern) == 3 and sorted(pattern) == triad_intervals:
                chord_pattern = pattern_name
                break
        
        chord_type = triad_type_mapping.get(chord_pattern, "unknown")
        
        # Compute accidental:
        major_root = major_scale_notes[i]
        current_idx = note_names.index(root)
        major_idx = note_names.index(major_root)
        diff = current_idx - major_idx
        
        # Adjust diff to minimal steps:
        if diff > 6:
            diff -= 12
        elif diff < -6:
            diff += 12
        
        accidental = ""
        if diff < 0:
            accidental = "b" * abs(diff)
        elif diff > 0:
            accidental = "#" * diff
        
        # Determine Roman numeral case and notation:
        roman_base = grades[i]
        if chord_type == "minor":
            roman_case = roman_base.lower()
        else:
            roman_case = roman_base
        
        # Add diminished symbol:
        if chord_type == "diminished":
            notation_str = f"{accidental}{roman_case.lower()}°"
        else:
            notation_str = f"{accidental}{roman_case}"
        
        chords.append((root, chord_type, notation_str))
    
    return chords