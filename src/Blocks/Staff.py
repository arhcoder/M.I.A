from Note import get_times
from Phrase import Phrase
from Chord import Chord

class Staff:

    def __init__(self, signature: tuple, key_name: str, key_type=1, upbeat=0, tuning=440):
        """
            Represents a staff bar with a specific time signature and key
            Parameters:
                - signature [tuple]: A tuple representing the time signature (numerator, denominator)
                    Example: [4, 4] for 4/4 time.
                - key_name [str]: The name of the key ("C", "G#", "Bb", etc)
                - key_type [int]: The type of the key, where 1 represents major and 0 represents minor
                - upbeat [int]: The space occupied by the upbeat (anacrusis).
                    Must be between 0 and the second value of the signature.
                - tuning [int]: The tuning frequency, either 440 or 432 Hz
        """

        #? Signature:
        if not isinstance(signature, tuple) or len(signature) != 2:
            raise TypeError(f"\"signature\" must be a tuple of two integers, but given {signature}")
        
        numerator, denominator = signature
        if not (isinstance(numerator, int) and numerator > 0):
            raise ValueError(f"\"signature\" numerator must be a positive integer, but given {numerator}")  
        if denominator not in [2, 4, 8, 16, 32, 64]:
            raise ValueError(f"\"signature\" denominator must be one of [2, 4, 8, 16, 32, 64], but given {denominator}")
        self._signature = signature

        #? Key:
        if not isinstance(key_name, str):
            raise TypeError(f"\"key_name\" must be a string, but given {type(key_name).__name__}")
        
        # Converting all flats on sharps:
        naturals = ["C", "D", "E", "F", "G", "A", "B"]
        sharps = ["C#", "D#", "F#", "G#", "A#"]
        flats = ["Db", "Eb", "Gb", "Ab", "Bb"]
        key_name = key_name.capitalize()
        if key_name in flats:
            key_name = sharps[flats.index(key_name)]
        if key_name not in naturals + sharps + flats:
            raise ValueError(f"\"key_name\" must be one of {naturals + sharps + flats}, but given {key_name}")

        if key_type not in [0, 1]:
            raise ValueError(f"\"key_type\" must be 1 for major or 0 for minor, but given {key_type}")
        self._key = (key_name, "major" if key_type == 1 else "minor")

        #? Tuning:
        if tuning not in [440, 432]:
            raise ValueError(f"\"tuning\" must be either 440 or 432, but given {tuning}")
        self._tuning = tuning

        #? Upbeat:
        if not isinstance(upbeat, int):
            raise TypeError(f"\"upbeat\" must be an integer, but given {type(upbeat).__name__}")
        
        max_upbeat = denominator
        if not (0 <= upbeat <= max_upbeat):
            raise ValueError(f"\"upbeat\" must be between 0 and {max_upbeat}, but given {upbeat}")
        
        self._upbeat = upbeat
        self._anacrusis = True if upbeat != 0 else False

        # Calculate Space Per Bar:
        _, space_of_note = get_times(denominator)
        self._space_per_bar = numerator * space_of_note

        # Initialize Containers:
        self._content = []
        self._space = 0
        self._bars_amount = 0
    

    #/ GETTERS:
    #? SIGNATURE:
    @property
    def signature(self):
        return self._signature
    
    @signature.setter
    def signature(self, value):
        if not isinstance(value, tuple) or len(value) != 2:
            raise TypeError(f"\"signature\" must be a tuple of two integers, but given {value}")
        
        numerator, denominator = value
        if not (isinstance(numerator, int) and numerator > 0):
            raise ValueError(f"\"signature\" numerator must be a positive integer, but given {numerator}")
        
        if denominator not in [2, 4, 8, 16, 32, 64]:
            raise ValueError(f"\"signature\" denominator must be one of [2, 4, 8, 16, 32, 64], but given {denominator}")
        
        self._signature = value
        self._space_per_bar = numerator * get_times(denominator)[1]
        self._update_bars_amount()

    #? KEY:
    @property
    def key(self):
        return self._key
    
    @key.setter
    def key(self, value):
        if not (isinstance(value, tuple) and len(value) == 2):
            raise TypeError(f"\"key\" must be a tuple of (str, 'major'/'minor'), but given {value}")
        
        key_name, key_type = value
        if not isinstance(key_name, str):
            raise TypeError(f"\"key_name\" must be a string, but given {type(key_name).__name__}")
        
        if key_type not in ["major", "minor"]:
            raise ValueError(f"\"key_type\" must be 'major' or 'minor', but given {key_type}")
        
        self._key = (key_name.capitalize(), key_type)

    #? UPBEAT:
    @property
    def upbeat(self):
        return self._upbeat
    
    @upbeat.setter
    def upbeat(self, value):
        if not isinstance(value, int):
            raise TypeError(f"\"upbeat\" must be an integer, but given {type(value).__name__}")
        
        max_upbeat = self._signature[1]
        if not (0 <= value <= max_upbeat):
            raise ValueError(f"\"upbeat\" must be between 0 and {max_upbeat}, but given {value}")
        
        self._upbeat = value
        self._anacrusis = True if value != 0 else False
        self._update_bars_amount()

    #? ANACRUSIS:
    @property
    def anacrusis(self):
        return self._anacrusis

    #? TUNING:
    @property
    def tuning(self):
        return self._tuning
    
    @tuning.setter
    def tuning(self, value):
        if value not in [440, 432]:
            raise ValueError(f"\"tuning\" must be either 440 or 432, but given {value}")
        self._tuning = value
        # Potentially, update tuning in all elements:
        for element in self._content:
            if isinstance(element, Phrase):
                for note in element.notes:
                    note.tuning = self._tuning
            elif isinstance(element, Chord):
                element.tuning = self._tuning

    #? SPACE:
    @property
    def space(self):
        return self._space

    #? BARS AMOUNT:
    @property
    def bars_amount(self):
        return self._bars_amount

    def _update_bars_amount(self):
        self._bars_amount = self._space / self._space_per_bar

    def _update_space(self):
        self._space = sum(element.space for element in self._content)
        self._update_bars_amount()

    def _get_time_from_space(self, space_required):
        """
            Find the appropriate time value that corresponds to the given space.
            Parameters:
                - space_required [float]: The space to match
            Returns:
                - time [int]: The time value corresponding to the space
        """
        TIMES = {
            1: ("Whole", 64),
            2: ("Half", 32),
            4: ("Quarter", 16),
            8: ("Eighth", 8),
            16: ("Sixteenth", 4),
            32: ("Thirty-second", 2),
            64: ("Sixty-fourth", 1),
            3: ("Half Triplet", 21.33),
            6: ("Quarter Triplet", 10.66),
            12: ("Eighth Triplet", 5.33),
            24: ("Sixteenth Triplet", 2.66),
        }
        for time, (_, space) in TIMES.items():
            if abs(space - space_required) < 1e-2:
                return time
        raise ValueError(f"No matching time found for space: {space_required}")
    

    def __repr__(self):
        return (
            f"Staff(signature={self._signature}, key={self._key}, tuning={self._tuning}, "
            f"upbeat={self._upbeat}, anacrusis={self._anacrusis}, space={self._space}, "
            f"bars_amount={self._bars_amount}, elements={self._content})"
        )