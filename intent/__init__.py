import pickle

import spacy
import numpy as np

with open('intent_model.pickle', 'rb') as input:
    model, le = pickle.load(input)

nlp = spacy.load('en_core_web_md', exclude=[
                 'tagger', 'parser', 'attribute_ruler', 'lemmatizer', 'ner'])


def encode_messages(messages, nlp=nlp):
    X = np.zeros((len(messages), nlp.vocab.vectors_length))
    # Iterate over the messages
    for idx, message in enumerate(messages):
        # Pass each message to the nlp object to create a document
        doc = nlp(message)
        # Save the document's .vector attribute to the corresponding row in X
        X[idx, :] = doc.vector
    return X

def predict_intent(message):
    X = encode_messages([message])
    probabilities = model.predict_proba(X)[0]
    max_value = np.max(probabilities)
    max_index = np.where(probabilities == max_value)[0]
    if (max_value <= 0.35):
        return 'unknown'
    return le.inverse_transform(max_index)[0]

if __name__ == '__main__':
	print(predict_intent('chicken'))