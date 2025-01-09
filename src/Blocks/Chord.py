from Note import Note
patterns = ["", "m", "7", "maj7", "m7", "mmaj7", "aug", "dim", "sus2", "sus4", "9", "maj9", "m9", "11", "maj11", "m11", "13", "maj13", "m13", "dim7", "m7b5", "add9", "madd9", "6", "m6", "aug7", "7b9", "7#9", "7b5", "7#5", "9#11"]

class Chord:

    def __init__(self, name: str, ctype: str, inversion: int, octave: int, time: int, dot: bool = False, tuning: int = 440):
        '''
            Paremeters:
            - name [str]: Indicates the name of the chord based on the root note.
                It could be some of this values:
                ["C", "D", "E", "F", "G", "A", "B"]
                Or some of this values:
                ["C#", "D#", "F#", "G#", "A#"] or ["Db", "Eb", "Gb", "Ab", "Bb"]
                "X" value represents a silent chords.
            - ctype [str]: The type of the chord. It could be:
                
                Value       | Description
                ------------|-----------------------------------------
                ""          | Major chord (empty string)
                "m"         | Minor chord
                "7"         | Dominant 7th chord
                "maj7"      | Major 7th chord
                "m7"        | Minor 7th chord
                "mmaj7"     | Minor Major 7th chord
                "aug"       | Augmented chord
                "dim"       | Diminished chord
                "sus2"      | Suspended 2nd chord
                "sus4"      | Suspended 4th chord
                "9"         | Dominant 9th chord
                "maj9"      | Major 9th chord
                "m9"        | Minor 9th chord
                "11"        | Dominant 11th chord
                "maj11"     | Major 11th chord
                "m11"       | Minor 11th chord
                "13"        | Dominant 13th chord
                "maj13"     | Major 13th chord
                "m13"       | Minor 13th chord
                "dim7"      | Diminished 7th chord
                "m7b5"      | Half-Diminished 7th chord (Minor 7 flat 5)
                "add9"      | Add 9 chord
                "madd9"     | Minor Add 9 chord
                "6"         | Major 6th chord
                "m6"        | Minor 6th chord
                "aug7"      | Augmented 7th chord
                "7b9"       | Dominant 7 flat 9 chord
                "7#9"       | Dominant 7 sharp 9 chord
                "7b5"       | Dominant 7 flat 5 chord
                "7#5"       | Dominant 7 sharp 5 chord
                "9#11"      | Dominant 9 sharp 11 chord

            - inversion [int] Indicates if the chord has an inversion (only between 0 and 3):
                - If 0, it will be in fundamental state.
                - If 1, 2 or 3, it will be applied the inversions.
            - octave [int]: Octave of the chord root (before apply an inversion).
            - time [int]: Base time value for the chord:

                Time   | Figure Name
                -------|-------------------
                1      | Whole
                2      | Half
                4      | Quarter
                8      | Eighth
                16     | Sixteenth
                32     | Thirty-second
                64     | Thirty-fourth
                3      | Half Triplet
                6      | Quarter Triplet
                12     | Eighth Triplet
                24     | Sixteenth Triplet

        '''

        #/ ATTRIBUTES:
        #? Chord name:
        naturals = ["C", "D", "E", "F", "G", "A", "B", "X"]
        sharps = ["C#", "D#", "F#", "G#", "A#"]
        flats = ["Db", "Eb", "Gb", "Ab", "Bb"]
        name = name.capitalize()
        if name in flats:
            name = sharps[flats.index(name)]
        if name not in naturals + sharps + flats:
            raise ValueError(f"\"name\" must be one of {naturals + sharps + flats}, but given {name}")
        self._name = name
        
        #? Chord type:
        ctype = ctype.lower()
        if ctype not in patterns:
            raise ValueError(f"\"ctype\" must be one of {patterns}, but given {ctype}")
        self._ctype = ctype

        #? Chord inversion:
        if inversion < 0 or inversion > 3 or not isinstance(inversion, int):
            raise ValueError(f"\"inversion\" must be an integer between 0 and 3, but given {inversion}")
        self._inversion = inversion

        #? Root octave:
        if octave < 0 or octave > 8 or not isinstance(octave, int):
            raise ValueError(f"\"octave\" must be an integer between 0 and 8, but given {octave}")
        self._octave = octave

        #? Chord time:
        if time not in [1, 2, 4, 8, 16, 32, 64, 3, 6, 12, 24]:
            raise ValueError(f"\"time\" must be one of: [1, 2, 4, 8, 16, 32, 64] or for tripletes: [3, 6, 12, 24], but given {time}")
        self._time = time

        #? Existance of Dot in the note:
        if not isinstance(dot, bool):
            raise TypeError(f"\"dot\" has to be boolean (True or False), but given {dot}")
        self._dot = dot

        #? Chord tuning:
        if tuning not in [440, 432]:
            raise ValueError(f"\"tuning\" must be either 440 or 432, but given {tuning}")
        self._tuning = tuning

        #? Calculated:
        self._notes = None
        self._notes_str = None
        self._calculate_notes()
    

    #/ METHODS:
    def _calculate_notes(self):

        # If silent chord, ignore the rest:
        if self._name == "X":
            self._ctype = None
            self._inversion = None
            self._octave = None
            self._notes = [Note(self._time, "X", 0, self._dot, self._tuning)]
            self._notes_str = []
            return

        #? Constants:
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        patterns = {
            "": [0, 4, 7],
            "m": [0, 3, 7],
            "7": [0, 4, 7, 10],
            "maj7": [0, 4, 7, 11],
            "m7": [0, 3, 7, 10],
            "mmaj7": [0, 3, 7, 11],
            "aug": [0, 4, 8],
            "dim": [0, 3, 6],
            "sus2": [0, 2, 7],
            "sus4": [0, 5, 7],
            "9": [0, 4, 7, 10, 14],
            "maj9": [0, 4, 7, 11, 14],
            "m9": [0, 3, 7, 10, 14],
            "11": [0, 4, 7, 10, 14, 17],
            "maj11": [0, 4, 7, 11, 14, 17],
            "m11": [0, 3, 7, 10, 14, 17],
            "13": [0, 4, 7, 10, 14, 17, 21],
            "maj13": [0, 4, 7, 11, 14, 17, 21],
            "m13": [0, 3, 7, 10, 14, 17, 21],
            "dim7": [0, 3, 6, 9],
            "m7b5": [0, 3, 6, 10],
            "add9": [0, 4, 7, 14],
            "madd9": [0, 3, 7, 14],
            "6": [0, 4, 7, 9],
            "m6": [0, 3, 7, 9],
            "aug7": [0, 4, 8, 10],
            "7b9": [0, 4, 7, 10, 13],
            "7#9": [0, 4, 7, 10, 15],
            "7b5": [0, 4, 6, 10],
            "7#5": [0, 4, 8, 10],
            "9#11": [0, 4, 7, 10, 14, 18]
        }

        # Gets the root and the intervals:
        root_index = scale.index(self._name)
        intervals = patterns[self._ctype]
        notes = []
        notes_obj = []
        notes_str = []
        current_octave = self._octave

        # Get each note of the chord:
        for _, interval in enumerate(intervals):
            note_index = (root_index + interval) % len(scale)
            note_name = scale[note_index]

            # Adjust the octave:
            if root_index + interval >= len(scale):
                current_octave += 1

            notes.append({"note": note_name, "octave": current_octave})

        # Apply inversions:
        for _ in range(self._inversion):
            inverted_note = notes.pop(0)
            inverted_note["octave"] += 1
            notes.append(inverted_note)
        

        # Creates two lists for notes:
        for note in notes:
            # Append the note using class Note:
            notes_obj.append(Note(self._time, note["note"], note["octave"], self._dot, self._tuning))

            # Generates also a easy lecture of the chord notes:
            notes_str.append(f'{note["note"]}{note["octave"]}')

        self._notes = notes_obj
        self._notes_str = notes_str
    

    #/ SETTERS:
    #? NAME:
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        naturals = ["C", "D", "E", "F", "G", "A", "B", "X"]
        sharps = ["C#", "D#", "F#", "G#", "A#"]
        flats = ["Db", "Eb", "Gb", "Ab", "Bb"]
        value = value.capitalize()
        if value in flats:
            value = sharps[flats.index(value)]
        if value not in naturals + sharps + flats:
            raise ValueError(f"\"name\" must be one of {naturals + sharps + flats}, but given {value}")
        if value != self._name:
            self._name = value
            self._calculate_notes()
    
    #? CTYPE:
    @property
    def ctype(self):
        return self._ctype
    
    @ctype.setter
    def ctype(self, value):
        value = value.lower()
        if value not in patterns:
            raise ValueError(f"\"value\" must be one of {patterns}, but given {value}")
        if value != self._ctype:
            self._ctype = value
            self._calculate_notes()
    
    #? CHORD INVERSION:
    @property
    def inversion(self):
        return self._inversion
    
    @inversion.setter
    def inversion(self, value):
        if value < 0 or value > 3 or not isinstance(value, int):
            raise ValueError(f"\"inversion\" must be an integer between 0 and 3, but given {value}")
        if value != self._inversion:
            self._inversion = value
            self._calculate_notes()
    
    #? OCTAVE:
    @property
    def octave(self):
        return self._octave

    @octave.setter
    def octave(self, value):
        if value < 0 or value > 8 or not isinstance(value, int):
            raise ValueError(f"\"octave\" must be an integer between 0 and 8, but given {value}")
        if value != self._octave:
            self._octave = value
            self._calculate_notes()

    #? TIME:
    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self, value):
        if value not in [1, 2, 4, 8, 16, 32, 64, 3, 6, 12, 24]:
            raise ValueError(f"\"time\" must be one of: [1, 2, 4, 8, 16, 32, 64] or for tripletes: [3, 6, 12, 24], but given {value}")
        if value != self._time:
            self._time = value
            self._calculate_notes()
    
    #? DOT:
    @property
    def dot(self):
        return self._dot

    @dot.setter
    def dot(self, value):
        if not isinstance(value, bool):
            raise TypeError(f"\"dot\" has to be boolean (True or False), but given {value}")
        if value != self._dot:
            self._dot = value
            self._calculate_notes()
    
    #? TUNING:
    @property
    def tuning(self):
        return self._tuning

    @tuning.setter
    def tuning(self, value):
        if value not in [440, 432]:
            raise ValueError(f"\"tuning\" must be either 440 or 432, but given {value}")
        if value != self._tuning:
            self._tuning = value
            self._calculate_notes()
    

    def __repr__(self):
        return (
            f"Chord(name={self._name}, ctype={self._ctype}, inversion={self._inversion}, "
            f"octave={self._octave}, time={self._time}, dot={self._dot} notes={self._notes}, notes_str={self._notes_str})"
        )