#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pickle
import os
import sys
from builder import NLTKPreprocessor, identity

# Load model
model_file = 'model.pkl'
with open(model_file, 'rb') as f:
    model = pickle.load(f)

def model_predict(text):
    output = model.predict(pd.Series([text]))
    probability = model.predict_proba(pd.Series([text]))[0][output][0]
    answer = model.labels_.inverse_transform([output])[0][0]
    if probability < 0.02:
        answer = 'Thank you for your question. A live agent will get back to you shortly.'
    return answer



if __name__ == "__main__":
	# Ask your question here
	model_predict('How do I renew my subscription?')





