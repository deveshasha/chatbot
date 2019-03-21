#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import pickle
import os
import sys
from builder import NLTKPreprocessor, identity

class QnaBot():
	def __init__(self, model):
		with open(model, 'rb') as f:
		    self.model = pickle.load(f)

	def answer(self, text):
		output = self.model.predict(pd.Series([text]))
		probability = self.model.predict_proba(pd.Series([text]))[0][output][0]
		answer = self.model.labels_.inverse_transform([output])[0][0]
		# print(answer, probability)
		if probability < 0.02:
			answer = 'Thank you for your question. A live agent will get back to you shortly.'
		return answer
    

if __name__ == "__main__":
	# Ask your question here
	qna = QnaBot('model.pkl')
	# print(qna.answer('How do I renew my subscription?'))
	print(qna.answer('Charged for mobileshare usage, why?'))





