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
		self.threshold = 0.015

	def answer(self, text, verbose=False):
		output = self.model.predict(pd.Series([text]))
		probability = self.model.predict_proba(pd.Series([text]))[0][output][0]
		answer = self.model.labels_.inverse_transform([output])[0][0]
		if verbose: print(answer, probability)
		if probability < self.threshold:
			answer = 'Thank you for your question. A live agent will get back to you shortly.'
		return answer

	def setThres(self, val):
		self.threshold = val

if __name__ == "__main__":
	# Ask your question here
	qna = QnaBot('model.pkl')
	print(qna.answer('How do I renew my subscription?'))
	# print(qna.answer('Why does my internet connection keeps disconnecting?'))





