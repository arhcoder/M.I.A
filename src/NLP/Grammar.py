from nltk import CFG # type: ignore
from rules import sentences_rules
from words import complete_sentence
import random

class Grammar:

    def __init__(self, sentence_type):
        """
            Creates a Free-Context Grammar capable of generate sentences based on the type of sentence
            FOR NOW BASED PURELY ON SPANISH SENTENCES

            Parameters:
                - sentence_type [int]: Which kind of sentenceIt could be:
                    - 1: Simple Declarative Sentences
                    - 2: Simple Interrogative Sentences
                    - 3: Exclamative Sentences
                    - 4: Imperative Sentences
            
            Methods:
                - generate(): Returns a random sentence
                    [list[dict]]: List of dictionaries of the selected words, and its characteristics
                    Each element contains:
                        - "word" [str]: Selected word
                        - "syllables" [list[str]]: List of words syllables as string 
                        - "tonic" [int]: Number of the tonic syllable (NOTATION STARTING FROM 0)
        """

        #? Validations:
        if not (1 <= sentence_type <= len(sentences_rules)):
            raise ValueError(f"\"sentence_type\" must be an integer between 1 and {len(sentences_rules)}")

        #? Starts the grammar:
        self.title, grammar_rules = sentences_rules[sentence_type - 1]
        self.grammar = CFG.fromstring(grammar_rules)
        self.sentence_type = sentence_type
    

    def generate(self):
        """
            Generates a random sentence [str] based on PoS categories.

            Returns:
            - [list[dict]]: List of dictionaries of the selected words, and its characteristics
              Each element contains:
                - "word" [str]: Selected word
                - "syllables" [list[str]]: List of words syllables as string 
                - "tonic" [int]: Number of the tonic syllable (NOTATION STARTING FROM 0)
        """
        productions = self.grammar.productions()
        nonterminals = [prod.lhs() for prod in productions]
        def generate_random(symbol):
            choices = [prod for prod in productions if prod.lhs() == symbol]
            chosen = random.choice(choices)
            result = []
            for sym in chosen.rhs():
                if sym in nonterminals:
                    result.extend(generate_random(sym))
                else:
                    result.append(str(sym))
            return result
        
        #/ Example of return: "Det Sus Adj VConj Adv"
        sentence = generate_random(self.grammar.start())

        return complete_sentence(" ".join(sentence))