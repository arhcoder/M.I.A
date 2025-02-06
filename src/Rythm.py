import random
import math
import copy
from Data.rythm.times import TIMES
from Selectors import ewrs
from conf import simulated_annealing_phrases_params


class Rythm:

    def __init__(self, signature, upbeat):
        """

            This class allows to create an object that fits sentences (divided by syllables),
            into bars, giving ryhtmic figures to each syllable

            Parameters:
                - signature [tuple]: Time signature on the phrase. For example: (4, 4)
                - upbeat: [int]: Space occupied by the upbeat (anacrusis)
        """
        self.signature = signature
        self.upbeat = upbeat
        self.params = simulated_annealing_phrases_params
        self.TIMES = TIMES
        self.triplet_types = {3, 6, 12, 24}
    

    def preprocess_syllables(self, sentence):
        """
        Preprocess the sentence to apply synalepha. In this context the sentence is a list of tokens,
        where " " indicates a word boundary. Synalepha is applied as follows:
        
            - For each word (a sequence of tokens separated by " "), check whether the last character
              (ignoring the stress marker "*") of the last syllable of the previous word is a vowel and
              the first character of the first syllable of the current word is also a vowel.
            - If so, merge these two syllables. If either syllable was stressed (contains "*"),
              ensure the merged syllable is marked as stressed
        
        Returns:
            [list]: Processed syllable strings (with synalepha applied)
        """
        vowels = set("aeiouAEIOU")
        words = []
        current_word = []
        for token in sentence:
            if token == " ":
                if current_word:
                    words.append(current_word)
                    current_word = []
            else:
                current_word.append(token)
        if current_word:
            words.append(current_word)

        processed_syllables = []
        for syl in words[0]:
            processed_syllables.append(syl)

        # For subsequent words, apply synalepha between the last syllable of the previous word
        # and the first syllable of the current word:
        for word in words[1:]:
            first_syl = word[0]
            prev_text = processed_syllables[-1]

            # Remove stress marker for checking vowels:
            prev_clean = prev_text.replace("*", "")
            first_clean = first_syl.replace("*", "")
            if prev_clean and first_clean and (prev_clean[-1] in vowels) and (first_clean[0] in vowels):
                merged = prev_text + first_syl
                if ("*" in prev_text) or ("*" in first_syl):
                    if "*" not in merged:
                        merged = "*" + merged
                processed_syllables[-1] = merged
            else:
                processed_syllables.append(first_syl)
            for syl in word[1:]:
                processed_syllables.append(syl)
        return processed_syllables
    

    def fit(self, sentence, bars):
        """
            Fits a sentence into an amount of bars using Simulated Annealing

            Parameters:
                - sentence [list[str]]: Sentence in wich each element is a syllable
                    - A " " (space) element means an empty space between words
                    - A syllable with a "*" means it is stressed (tonic syllable)
                - bars [int]: Amount of bars in which the sentence must be fitted

            Returns:
                [tuple]: (initial_rest, syllable_figures, final_rest)
                    - initial_rest [int]: Figure time id number of the silence before the phrase
                    - syllable_figures [list]: Note IDs (integers) assigned to each syllable (non-space)
                    - final_rest [int]: Figure id number of the silence after the phrase
                    - dots [list[bool]]: For each syllable, True if the note is dotted, else False
                        (The first and last entries correspond to the rests.)
                
                    NOTE: FOR FIGURE TIME ID NUMBERS:

                    Time   | Figure Name
                    -------|-------------------
                    1      | Whole
                    2      | Half
                    4      | Quarter
                    8      | Eighth
                    16     | Sixteenth
                    32     | Thirty-second
                    64     | Sixty-fourth
                    3      | Half Triplet
                    6      | Quarter Triplet
                    12     | Eighth Triplet
                    24     | Sixteenth Triplet
        """
        # Preprocess sentence (apply synalepha):
        syllables = self.preprocess_syllables(sentence)
        num_syllables = len(syllables)

        # Calculate the total available "space" in our time system:
        denom = self.signature[1]
        if denom not in self.TIMES:
            raise ValueError(f"Wrong Time Signature: Denom {denom} must be one of {list(TIMES.keys())}")
        base_duration = self.TIMES[denom][1]
        beats_per_bar = self.signature[0]
        bar_space = beats_per_bar * base_duration
        total_space = bars * bar_space

        # Generate an initial candidate solution:
        candidate = self._generate_initial_solution(num_syllables)

        # Run simulated annealing.
        best_candidate = self._simulated_annealing(candidate, syllables, total_space)

        # best_candidate is a tuple: (notes, dots):
        notes, dots = best_candidate

        # notes[0] is the initial rest, notes[1:-1] are the syllable notes, notes[-1] is the final rest:
        return notes[0], notes[1:-1], notes[-1], dots
    

    def _generate_initial_solution(self, num_syllables):
        """
            Generates an initial candidate solution

            Returns a tuple (notes, dots) where:
                - notes [list]: List of length num_syllables + 2 (positions 0 and -1 are rests)
                - dots [list]: List of booleans of the same length, where each entry indicates if that note is dotted
            
            Each note is chosen using the exponential selection function. For syllable notes, a dot flag
            is assigned with probability given by self.params["dot_probability"]. For rests, dot is always False
        """

        allowed = list(self.TIMES.keys())
        x_param = self.params.get("selection_bias", 1)
        dot_prob = self.params.get("dot_probability", 0.15)

        notes = []
        dots = []

        # Generate initial rest:
        initial_rest = ewrs(allowed, x_param)
        notes.append(initial_rest)
        dots.append(random.random() < dot_prob)

        # Generate syllable notes:
        for _ in range(num_syllables):
            note = ewrs(allowed, x_param)
            notes.append(note)
            dots.append(random.random() < dot_prob)

        # Generate final rest:
        final_rest = ewrs(allowed, x_param)
        notes.append(final_rest)
        dots.append(random.random() < dot_prob)

        return (notes, dots)
    

    def _simulated_annealing(self, candidate, syllables, total_space):
        """
            Runs the simulated annealing loop
            The candidate is represented as a tuple: (notes, dots)
        """
        current = candidate
        current_score = self.rate(current, syllables, total_space)
        best = copy.deepcopy(current)
        best_score = current_score

        T = self.params.get("initial_temperature", 100.0)
        cooling_rate = self.params.get("cooling_rate", 0.99)
        iterations = self.params.get("iterations", 1000)

        for _ in range(iterations):
            neighbor = self._neighbor(current)
            score = self.rate(neighbor, syllables, total_space)
            if score > current_score or random.uniform(0, 1) < math.exp((score - current_score) / T):
                current = neighbor
                current_score = score
                if score > best_score:
                    best = copy.deepcopy(neighbor)
                    best_score = score
            T *= cooling_rate

        return best
    

    def _neighbor(self, candidate):
        """
            Returns a neighboring candidate solution by randomly changing one element
            Candidate is a tuple (notes, dots)
        
            A random index is selected from 0 to len(notes)-1. For rests (indices 0 and -1),
            only the note ID is updated (the dot flag remains False). For a syllable note,
            both its note ID and dot flag are updated. Additionally, if the new note is a
            triplet type and there are at least two following syllable notes, the neighbor
            forces the next two syllable notes (and their dot flags) to match
        """

        notes, dots = candidate
        new_notes = notes.copy()
        new_dots = dots.copy()

        index = random.randint(0, len(new_notes) - 1)
        allowed = list(self.TIMES.keys())
        x_param = self.params.get("selection_bias", 1)
        new_value = ewrs(allowed, x_param)
        dot_prob = self.params.get("dot_probability", 0.15)

        # Update both note and dot flag at the chosen index:
        new_notes[index] = new_value
        new_dots[index] = (random.random() < dot_prob)

        # If the changed index corresponds to a syllable note (indices 1 to len(notes)-2)
        # and the new note is a triplet type, force the next two syllable notes (if available) to match:
        if 1 <= index <= len(new_notes) - 2:
            if new_value in self.triplet_types and (index <= len(new_notes) - 3):
                new_notes[index + 1] = new_value
                new_notes[index + 2] = new_value
                new_dots[index + 1] = new_dots[index]
                new_dots[index + 2] = new_dots[index]
        
        return (new_notes, new_dots)
    

    def rate(self, candidate, syllables, total_space):
        """
            Objective function to rate the candidate solution

            Parameters:
                - candidate [tuple]: (notes, dots)
                    - notes: list[int] of length num_syllables+2
                    - dots: list[bool] of length num_syllables (for syllable notes)
                - syllables [list[str]]: Syllable strings corresponding to candidate notes positions 1..-2.
                - total_space [int]: Total required space (based on bars and time signature)

            The function:
                - Penalizes the difference between the computed space and total_space
                - For syllable notes, if dotted, half the note's duration is added:
                    - Rewards placing stressed syllables ("*") on strong beats (adjusted by upbeat)
                    - Penalizes candidates violating triplet constraints
                    - Rewards longer rests (initial and final) and handles uniformity versus variety

                Returns:
                    [float]: A score (higher is better).
        """
        notes, dots = candidate
        score = 0

        #? 1. Total space calculation:
        computed_space = 0
        for idx, note in enumerate(notes):
            duration = self.TIMES[note][1]
            if dots[idx]:
                duration += 0.5 * self.TIMES[note][1]
            computed_space += duration
        space_weight = self.params.get("space_weight", 1)
        score -= abs(computed_space - total_space) * space_weight

        #? 2. Reward stressed syllables on strong beats:
        base_duration = self.TIMES[self.signature[1]][1]
        upbeat_duration = self.upbeat * base_duration
        bar_space = self.signature[0] * base_duration

        cum_time = self.TIMES[notes[0]][1]
        
        # Syllable notes are from indices 1 to len(notes)-2:
        for idx, syl in enumerate(syllables):
            note_duration = self.TIMES[notes[idx + 1]][1]
            if dots[idx + 1]:
                note_duration += 0.5 * self.TIMES[notes[idx + 1]][1]
            effective_position = (cum_time - upbeat_duration) % bar_space
            if "*" in syl:
                if effective_position < 2:
                    score += self.params.get("stress_reward", 10)
                else:
                    score -= self.params.get("stress_penalty", 5)
            cum_time += note_duration

        #? 3. Triplet constraints:
        triplet_penalty = self.params.get("triplet_penalty", 20)
        for i in range(1, len(notes) - 2):
            if notes[i] in self.triplet_types:
                if not (notes[i] == notes[i + 1] == notes[i + 2]):
                    score -= triplet_penalty

        #? 4. Rewards for initial and final silence:
        rest_reward_factor = self.params.get("rest_reward", 5)
        score += self.TIMES[notes[0]][1] * rest_reward_factor
        score += self.TIMES[notes[-1]][1] * rest_reward_factor

        #? 5. Uniformity vs. variety:
        uniformity_param = self.params.get("uniformity", 50)
        uniform_bonus = 0
        for i in range(1, len(notes) - 1):
            if i < len(notes) - 2 and notes[i] == notes[i + 1]:
                uniform_bonus += 1
            else:
                uniform_bonus -= 1
        score += uniform_bonus * (100 - uniformity_param) / 50

        return score