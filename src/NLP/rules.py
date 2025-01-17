
#/ PRODUCTION RULES FOR CONTEXT-FREE GRAMMARS OF SPANISH SENTENCES /#

#? [01]: Simple Declarative Sentences:
simple_declarative = ("Simple Declarative Sentence",
"""
S -> Sujeto Predicado

# Reglas para Sujeto:
Sujeto -> Det Sus | Det Sus Adj | PronPer | PronDem Sus | PronDem Sus Adj

# Reglas para Predicado:
Predicado -> Verbo Objeto Circunstancial | Verbo Objeto | Verbo Circunstancial | Verbo

# Reglas para Verbo:
Verbo -> VTran | VIntra | VConj | VCop Adj

# Reglas para Objeto:
Objeto -> Det Sus | Det Sus Adj | PronRef | PronPrep | Sus

# Reglas para Circunstancial:
Circunstancial -> Prep Sus | Prep Sus Adj | Adv

# Terminales (categorías gramaticales):
Det -> 'Det'
Sus -> 'Sus'
Adj -> 'Adj'
PronPer -> 'PronPer'
PronDem -> 'PronDem'
VTran -> 'VTran'
VIntra -> 'VIntra'
VCop -> 'VCop'
VConj -> 'VConj'
PronRef -> 'PronRef'
PronPrep -> 'PronPrep'
Prep -> 'Prep'
Adv -> 'Adv'
"""
)


#? [02] Simple Interrogative Sentences:
simple_interrogative = ("Simple Interrogative Sentence",
"""
# Oración Interrogativa Simplificada:
S -> PartInterr Verbo Sujeto Circunstancial
S -> PartInterr Verbo Sujeto
S -> PartInterr Verbo Objeto
S -> PartInterr Verbo
S -> Verbo Sujeto Objeto PartInterr
S -> Verbo Sujeto Circunstancial PartInterr
S -> PartInterr Sujeto Verbo

# Partículas Interrogativas:
PartInterr -> PronIntExc
PartInterr -> AdvInt

# Sujeto:
Sujeto -> PronPer
Sujeto -> PronDem
Sujeto -> Sus

# Verbo:
Verbo -> VTran
Verbo -> VIntra
Verbo -> VCop Adj
Verbo -> VConj
Verbo -> VCop

# Objeto:
Objeto -> Det Sus
Objeto -> PronRef
Objeto -> Sus

# Circunstancial:
Circunstancial -> Prep Sus
Circunstancial -> Adv

# Terminales (categorías gramaticales):
Det -> 'Det'
Sus -> 'Sus'
PronPer -> 'PronPer'
PronDem -> 'PronDem'
VTran -> 'VTran'
VIntra -> 'VIntra'
VCop -> 'VCop'
VConj -> 'VConj'
PronRef -> 'PronRef'
Prep -> 'Prep'
Adv -> 'Adv'
AdvInt -> 'PronIntExc'
PronIntExc -> 'PronIntExc'
"""
)


#? [03] Exclamative Sentences:
exclamative_sentence = ("Exclamative Sentence",
"""
# Oración Exclamativa Completa:
S -> Int PartExcl Verbo Sujeto Objeto Circunstancial
S -> Int PartExcl Verbo Sujeto Circunstancial
S -> Int PartExcl Verbo Sujeto Objeto
S -> Int PartExcl Verbo Sujeto
S -> Int PartExcl Sujeto Verbo Objeto Circunstancial
S -> Int PartExcl Sujeto Verbo Circunstancial
S -> Int PartExcl Sujeto Verbo Objeto
S -> Int PartExcl Sujeto Verbo
S -> PartExcl Verbo Sujeto Objeto Circunstancial
S -> PartExcl Verbo Sujeto Circunstancial
S -> PartExcl Sujeto Verbo Objeto
S -> PartExcl Sujeto Verbo Circunstancial
S -> PartExcl Verbo Objeto
S -> PartExcl Objeto
S -> PartExcl Circunstancial

# Partículas Exclamativas:
PartExcl -> PronIntExc
PartExcl -> AdvInt
PartExcl -> Adj

# Sujeto:
Sujeto -> Det Sus Adj
Sujeto -> Det Sus
Sujeto -> PronPer
Sujeto -> PronDem Sus
Sujeto -> Sus

# Verbo:
Verbo -> VTran
Verbo -> VIntra
Verbo -> VCop Adj
Verbo -> VCop
Verbo -> VConj

# Objeto:
Objeto -> Det Sus Adj
Objeto -> Det Sus
Objeto -> PronRef
Objeto -> PronPrep
Objeto -> Sus

# Circunstancial:
Circunstancial -> Prep Sus Adj
Circunstancial -> Prep Sus
Circunstancial -> Adv

# Interjecciones:
Int -> 'Int'

# Terminales (categorías gramaticales):
Det -> 'Det'
Sus -> 'Sus'
Adj -> 'Adj'
PronPer -> 'PronPer'
PronDem -> 'PronDem'
VTran -> 'VTran'
VIntra -> 'VIntra'
VCop -> 'VCop'
VConj -> 'VConj'
PronRef -> 'PronRef'
PronPrep -> 'PronPrep'
Prep -> 'Prep'
Adv -> 'Adv'
AdvInt -> 'PronIntExc'
PronIntExc -> 'PronIntExc'
Int -> 'Int'
"""
)


#? [04] Imperative Sentences:
imperative_sentence = ("Imperative Sentence",
"""
# Oración Imperativa Completa:
S -> VerboImp SujetoImplícito Objeto Circunstancial
S -> VerboImp Objeto Circunstancial
S -> VerboImp Circunstancial
S -> VerboImp Objeto
S -> SujetoExplícito VerboImp Objeto Circunstancial
S -> VerboImp
S -> SujetoExplícito VerboImp
S -> VerboImp SujetoImplícito

# Sujeto Implícito (omisión natural en oraciones imperativas):
SujetoImplícito -> ''

# Sujeto Explícito (cuando se necesita énfasis o claridad):
SujetoExplícito -> PronPer
SujetoExplícito -> Sus Det

# Verbo en Imperativo:
VerboImp -> 'VImp'

# Objeto (elementos directos que complementan el verbo):
Objeto -> Det Sus
Objeto -> Det Sus Adj
Objeto -> PronRef
Objeto -> PronDem
Objeto -> PronPer

# Circunstancial (complementos opcionales de lugar, tiempo o modo):
Circunstancial -> Prep Sus Adj
Circunstancial -> Prep Sus
Circunstancial -> Adv
"""
)

sentences_rules = [simple_declarative, simple_interrogative, exclamative_sentence, imperative_sentence]