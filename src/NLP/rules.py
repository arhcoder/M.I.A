
#/ PRODUCTION RULES FOR CONTEXT-FREE GRAMMARS OF SPANISH SENTENCES /#

#? [01]: Simple Declarative Sentences:
simple_declarative = ("Simple Declarative Sentence",
"""
S -> Sujeto Predicado

# Reglas para Sujeto:
Sujeto -> Det Sus Adj | PronPer | PronDem | Sus

# Reglas para Predicado:
Predicado -> Verbo Objeto Circunstancial | Verbo Objeto | Verbo Circunstancial | Verbo

# Reglas para Verbo:
Verbo -> VTran | VIntra | VCop

# Reglas para Objeto:
Objeto -> Det Sus Adj | PronRef | PronPrep | Sus

# Reglas para Circunstancial:
Circunstancial -> Prep Sus Adj | Prep Sus | Adv

# Terminales (categorías gramaticales):
Det -> 'Det'
Sus -> 'Sus'
Adj -> 'Adj'
PronPer -> 'PronPer'
PronDem -> 'PronDem'
VTran -> 'VTran'
VIntra -> 'VIntra'
VCop -> 'VCop'
PronRef -> 'PronRef'
PronPrep -> 'PronPrep'
Prep -> 'Prep'
Adv -> 'Adv'
""")


#? [02] Simple Interrogative Sentences:
simple_interrogative = ("Simple Interrogative Sentence",
"""
# Oración Interrogativa Completa:
S -> PartInterr Verbo Sujeto Objeto Circunstancial
S -> PartInterr Verbo Sujeto Objeto
S -> PartInterr Verbo Sujeto Circunstancial
S -> PartInterr Verbo Sujeto
S -> PartInterr Sujeto Verbo Objeto Circunstancial
S -> PartInterr Sujeto Verbo Objeto
S -> PartInterr Sujeto Verbo Circunstancial
S -> Verbo Sujeto Objeto Circunstancial PartInterr
S -> Verbo Sujeto Objeto PartInterr
S -> Verbo Sujeto Circunstancial PartInterr
S -> PartInterr Verbo

# Partículas Interrogativas:
PartInterr -> 'PronIntExc'
PartInterr -> 'Adv'

# Sujeto:
Sujeto -> Det Sus Adj
Sujeto -> 'PronPer'
Sujeto -> 'PronDem'
Sujeto -> 'Sus'

# Verbo:
Verbo -> 'VTran'
Verbo -> 'VIntra'
Verbo -> 'VCop'
Verbo -> 'VConj'

# Objeto:
Objeto -> Det Sus Adj
Objeto -> 'PronRef'
Objeto -> 'PronPrep'
Objeto -> 'Sus'

# Circunstancial:
Circunstancial -> Prep Sus Adj
Circunstancial -> Prep Sus
Circunstancial -> 'Adv'

# Determinantes:
Det -> 'Det'

# Sustantivos:
Sus -> 'Sus'

# Adjetivos:
Adj -> 'Adj'

# Preposiciones:
Prep -> 'Prep'

# Adverbios:
Adv -> 'Adv'

# Pronombres:
PronIntExc -> 'PronIntExc'
PronPer -> 'PronPer'
PronRef -> 'PronRef'
PronPrep -> 'PronPrep'
PronDem -> 'PronDem'
"""
)


#? [03] Exclamative Sentences:
exclamative_sentence = ("Exclamative Sentence",
"""
# Oración Exclamativa Completa:
S -> PartExcl Verbo Sujeto Objeto Circunstancial
S -> PartExcl Sujeto Verbo Objeto Circunstancial
S -> PartExcl Sujeto Verbo Circunstancial
S -> PartExcl Verbo Sujeto
S -> Verbo Sujeto Objeto Circunstancial PartExcl
S -> Sujeto Verbo PartExcl
S -> PartExcl Objeto
S -> PartExcl Circunstancial

# Partículas Exclamativas:
PartExcl -> 'PronIntExc' | 'Adv' | 'Adj'

# Sujeto:
Sujeto -> 'Det Sus Adj' | 'PronPer' | 'PronDem' | 'Sus'

# Verbo:
Verbo -> 'VTran' | 'VIntra' | 'VCop'

# Objeto:
Objeto -> 'Det Sus Adj' | 'PronRef' | 'PronPrep' | 'Sus'

# Circunstancial:
Circunstancial -> 'Prep Sus Adj' | 'Prep Sus' | 'Adv'
""")


#? [04] Imperative Sentences:
imperative_sentence = ("Imperative Sentence",
"""
# Oración Imperativa Completa:
S -> VerboImp SujetoImplícito Objeto Circunstancial
S -> VerboImp Objeto Circunstancial
S -> VerboImp Circunstancial
S -> SujetoExplícito VerboImp Objeto Circunstancial
S -> VerboImp Objeto
S -> VerboImp

# Sujeto Implícito:
SujetoImplícito -> ''

# Sujeto Explícito:
SujetoExplícito -> PronPer 'PronPer'
SujetoExplícito -> Sus Det 'Sus' 'Det'

# Verbo en Imperativo:
VerboImp -> 'VImp'

# Objeto:
Objeto -> Det Sus Adj 'Det' 'Sus' 'Adj'
Objeto -> PronRef 'PronRef'
Objeto -> PronDem 'PronDem'
Objeto -> PronPer 'PronPer'

# Circunstancial:
Circunstancial -> Prep Sus Adj 'Prep' 'Sus' 'Adj'
Circunstancial -> Prep Sus 'Prep' 'Sus'
Circunstancial -> Adv 'Adv'
""")

sentences_rules = [simple_declarative, simple_interrogative, exclamative_sentence, imperative_sentence]