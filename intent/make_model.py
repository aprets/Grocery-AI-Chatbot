import json

import pandas as pd
import numpy as np
import spacy

np.random.seed(0)

with open('dataset.json') as json_file:
    raw_dataset = json.load(json_file)
# with open('badset_test.json') as json_file:
#     raw_test = json.load(json_file)
    
tersed_dataset = [{'text': e['text'], 'intent': e['intentName']} for e in (raw_dataset['data'])]

dataset = pd.DataFrame(tersed_dataset)

# Exclude most of SpaCy's pipeline as we mostly only need vectors
nlp = spacy.load('en_core_web_md', exclude=['tagger','parser', 'attribute_ruler', 'lemmatizer', 'ner'])
print(nlp.meta['name'], nlp.meta['version'])
print(nlp.pipe_names)
print(spacy.__version__)

from sklearn.preprocessing import LabelEncoder

def encode_messages(messages, nlp=nlp):
    # Get vector length
    embedding_dim = nlp.vocab.vectors_length
    
    # Calculate number of messages
    n_messages = len(messages)

    print('Vectorising',n_messages, 'messages with spaCy .vector and encoding them...')

    X = np.zeros((n_messages, embedding_dim))

    # Iterate over the messages
    for idx, message in enumerate(messages):
        # Pass each message to the nlp object to create a document
        doc = nlp(message)
        # Save the document's .vector attribute to the corresponding row in X  
        X[idx, :] = doc.vector
    return X

def make_label_encoder(intents):
    print('Making new label encoder...')
    return LabelEncoder().fit(intents)

def encode_labels(labels, le):
    # Calculate the length of labels
    n_labels = len(labels)
    print('Encoding', n_labels, 'intent labels...')
    
    # instantiate labelencoder object
    y = le.transform(labels)
    return y

def get_tuning_params(y):
    defaults = {                 
    "C": [1, 2, 5, 10, 20, 100],
    "kernels": ["linear"],
    "max_cross_validation_folds": 5
    }
    C = defaults["C"]                       
    kernels = defaults["kernels"]
    tuned_parameters = [{"C": C, "kernel": [str(k) for k in kernels]}]                                                                 
    folds = defaults["max_cross_validation_folds"]
    cv_splits = max(2, min(folds, np.min(np.bincount(y)) // 5))
    print(tuned_parameters, cv_splits)
    return tuned_parameters, cv_splits

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

def svm_train(X,y, tuned_parameters, cv_splits):
    print('Training SVC...')
    # Create a support vector classifier
    clf = GridSearchCV(
        SVC(C=1, probability=True, class_weight='balanced'),
        param_grid=tuned_parameters,
        n_jobs=4,
        cv=cv_splits,
        scoring='f1_weighted',
        verbose=1,
    )

    # Fit the classifier using the training data
    clf.fit(X, y)
    return clf

train_data = dataset.sample(frac=1, random_state=0)

# preprocess data
# encode text to vectors
train_X = encode_messages(train_data.text, nlp)

le = make_label_encoder(train_data.intent.unique())

# convert intent text to int
train_y = encode_labels(train_data.intent, le)


# train the model
tuned_parameters, cv_splits = get_tuning_params(train_y)

model = svm_train(train_X, train_y, tuned_parameters, cv_splits)

import pickle

with open('intent.pickle', 'wb') as output:
	pickle.dump((model, le), output)