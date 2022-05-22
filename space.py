import spacy 


nlp = spacy.load('en_core_web_md')

doc = nlp('i want to buy a Dyson vacuum cleaner ')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

tokens = nlp("dog cat banana chicken bread afskfsd")

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm, token.is_oov)