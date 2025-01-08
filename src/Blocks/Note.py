import pandas as pd
frequencies_path = "../Data/frequencies.csv"

class Note:

    def __init__(self, time: int, note: str, octave: int, dot: bool = False, tuning: int = 440):
        '''
            Parameters:
            - time [int]: Base time value for the note:
                ----------------------
                1   Whole
                2   Half
                4   Quarter
                8   Eighth
                16  Sixteenth
                32  Thirty-second
                64  Sixty-fourth
                ----------------------
                3   Half Triplet
                6   Quarter Triplet
                12   Eighth Triplet
                24   Sixteenth Triplet
                ----------------------
            - note [str]: The name of the note ("C", "C#" or "Db", "D", etc.)
                If silence put "X"
            - octave [int]: Octave number (0–8)

            - dot [bool]: If True, add one have of the space of the note.
            - tuning [str]: Tuning frequency, either 440 (default) or 432 Hz.

            Raises:
            - ValueError: If the note or time value is invalid.
        '''

        #/ ATTRBIUTES:
        #? Time identifier for the note:
        if time not in [1, 2, 4, 8, 16, 32, 64, 3, 6, 12, 24]:
            raise ValueError(f"\"time\" must be one of: [1, 2, 4, 8, 16, 32, 64] or for tripletes: [3, 6, 12, 24], but given {time}")
        self._time = time

        #? Note name:
        self._note = str(note).capitalize()

        #? Note octave:
        if octave < 0 or octave > 8 or not isinstance(octave, int):
            raise ValueError(f"\"octave\" must be an integer between 0 and 8, but given {octave}")
        self._octave = octave

        #? Existance of Dot in the note:
        if not isinstance(dot, bool):
            raise TypeError(f"\"dot\" has to be boolean (True or False), but given {dot}")
        self._dot = dot

        #? Note tuning:
        if tuning not in [440, 432]:
            raise ValueError(f"\"tuning\" must be either 440 or 432, but given {tuning}")
        self._tuning = tuning

        self._frequency = None
        self._space = None
        self._name = None
        self._update_space()
        self._update_frequency()

    #/ METHODS:
    def _update_space(self):
        TIMES = {
            1: ("Whole", 64),
            2: ("Half", 32),
            4: ("Quarter", 16),
            8: ("Eighth", 8),
            16: ("Sixteenth", 4),
            32: ("Thirty-second", 2),
            64: ("Thirty-fourth", 1),

            3: ("Half Triplet", 21.33),
            6: ("Quarter Triplet", 10.66),
            12: ("Eighth Triplet", 5.33),
            24: ("Sixteenth Triplet", 2.66),
        }
        self._name, space = TIMES[self._time]
        if self._dot:
            self._space = space + space / 2
        else:
            self._space = space
    
    def _update_frequency(self):
        if self._note == "X":
            self._frequency = 0
            self._octave = 0
        else:
            try:
                frequencies = pd.read_csv(frequencies_path)
            except FileNotFoundError:
                raise FileNotFoundError(f"File \"{frequencies_path}\" not found")
            frequencies["normalized_notes"] = frequencies["note"].str.split().apply(set)
            for _, row in frequencies.iterrows():
                if self._note in row["normalized_notes"].union(row["note"].split()) and row["octave"] == self._octave:
                    self._frequency = float(row[f"f{self._tuning}"])
                    break
            else:
                raise ValueError(f"Invalid note \"{self._note}\" or octave \"{self._octave}\"")
    

    #/ SETTERS:
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
            self._update_space()
    
    #? NAME:
    @property
    def name(self):
        return self._name
    
    #? NOTE:
    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, value):
        if value != self._note:
            self._note = str(value).capitalize()
            self._update_frequency()
    
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
            self._update_frequency()
    
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
            self._update_space()
    
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
            self._update_frequency()

    #? SPACE:
    @property
    def space(self):
        return self._space
    
    #? FREQUENCY:
    @property
    def frequency(self):
        return self._frequency
    

    #/ PRINTING VARIABLES:
    def __repr__(self):
        return (f"Note(note={self._note}, octave={self._octave}, frequency={self._frequency} Hz, "
                f"time={self._time}, name={self._name} dot={self._dot} space={self._space}, tuning={self._tuning} Hz)")