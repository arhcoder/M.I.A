from Grammar import Grammar

#? FOR EACH KIND OF SENTENCE:
for sentence_type in [1, 2, 3, 4]:

    #? Creates the grammar:
    grammar = Grammar(sentence_type=sentence_type)
    print(f"\n[{sentence_type}] {grammar.title}")

    #? Generates 10 random sentences:
    for _ in range(10):
        gen_sentence = grammar.generate()
        sentence = " ".join([word["word"] for word in gen_sentence])
        print("*", sentence.capitalize())