from Blocks.Staff import Staff
from Blocks.Phrase import Phrase

class Melody(Staff):

    def __init__(self, signature: tuple, key_name: str, key_type=1, upbeat=0, tuning=440):
        """
            Represents a melody staff containing a list of Phrase objects
            Inherits from Staff
            Parameters:
                - signature [tupe]: Time signature
                - key_name [str]: Name of the key
                - key_type [int]: 1 for major, 0 for minor
                - upbeat [int]: Space occupied by the upbeat
                - tuning [int]: Tuning frequency
        """
        super().__init__(signature, key_name, key_type, upbeat, tuning)
    
    def add_element(self, phrase: Phrase):
        """
        Add a Phrase to the melody
        Parameters:
            - phrase [Phrase]: The Phrase object to add
        """
        if not isinstance(phrase, Phrase):
            raise TypeError("Element must be an instance of Phrase.")
        
        self._content.append(phrase)
        self._update_space()
    

    def __repr__(self):
        return (
            f"Melody(signature={self._signature}, key={self._key}, tuning={self._tuning}, "
            f"upbeat={self._upbeat}, anacrusis={self._anacrusis}, space={self._space}, "
            f"bars_amount={self._bars_amount}, phrases={self._content})"
        )
    
    def __repr__(self):
        return (
            "\nMelody(\n"
            f"    signature={self._signature},\n"
            f"    key={self._key},\n"
            f"    tuning={self._tuning},\n"
            f"    upbeat={self._upbeat},\n"
            f"    anacrusis={self._anacrusis},\n"
            f"    space={self._space},\n"
            f"    bars_amount={self._bars_amount},\n"
            f"    phrases=[\n"
            + ',\n'.join(['        ' + repr(phrase) for phrase in self._content]) + '\n'
            f"    ]\n"
            ")"
        )
