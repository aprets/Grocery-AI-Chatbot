import pickle

import spacy
import numpy as np

with open('intent.pickle', 'rb') as input:
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


def get_oneoff_prediction(message, model, le):
    X = encode_messages([message])
    return le.inverse_transform(model.predict(X))[0]


print(get_oneoff_prediction('restart', model, le))
