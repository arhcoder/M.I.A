from Note import Note

class Phrase:

    def __init__(self):
        '''
            To group notes in a way of melodic phrases

            Attributes:
                - space: [int] Space that take in sum of notes space
                - notes: [list]: List of orderer notes (Note object)

            Methods:
                - add_start(Note object): Add a Note() object in the start of notes list
                - add_end(Note object): Add a Note() object in the end of notes list
                - remove(index int): Remove the note of the index. If index=0, remove the first
                - replace(index int, Note object): Replace the note of index with a new one, If index=0, replace the first
        '''

        self._space = 0
        self._notes = []
        self._update_space()
    
    def _update_space(self):
        self._space = sum(note.time for note in self._notes)
    

    def add_start(self, note: Note):
        """
            Add a Note object at the start of the notes list

            Parameters:
                - note (Note): The Note object to add
        """
        if not isinstance(note, Note):
            raise TypeError("The parameter must be an instance of the Note class")
        self._notes.insert(0, note)
        self._update_space()

    def add_end(self, note: Note):
        """
            Add a Note object at the end of the notes list

            Parameters:
                - note (Note): The Note object to add
        """
        if not isinstance(note, Note):
            raise TypeError("The parameter must be an instance of the Note class")
        self._notes.append(note)
        self._update_space()
    
    def remove(self, index: int):
        """
        Remove a Note object by index from the notes list

        Parameters:
            - index (int): The index of the note to remove
        """
        if index < 0 or index >= len(self._notes):
            raise IndexError(f"Index {index} out of range")
        del self._notes[index]
        self._update_space()

    def replace(self, index: int, note: Note):
        """
        Modify a Note object by index in the notes list

        Parameters:
            - index (int): The index of the note to replace
            - note (Note): The new Note object to replace the existing one
        """
        if not isinstance(note, Note):
            raise TypeError("The parameter must be an instance of the Note class")
        if index < 0 or index >= len(self._notes):
            raise IndexError(f"Index {index} out of range")
        self._notes[index] = note
        self._update_space()
    

    #/ GETTERS:
    #? SPACE:
    @property
    def space(self):
        return self._space
    
    #? NOTES:
    @property
    def notes(self):
        return self._notes


    def __repr__(self):
        return f"Phrase(space={self._space}, notes={self._notes})"