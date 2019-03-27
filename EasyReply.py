from sklearn import metrics

import gensim
pathToBinVectors = 'GoogleNews-vectors-negative300.bin'

print ("Loading the data file... Please wait...")
model1 = gensim.models.KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)
print ("Successfully loaded 3.6 G bin file!")

import numpy as np
import math
from scipy.spatial import distance

from random import sample
import sys
from nltk.corpus import stopwords
import pandas as pd

# Convert sentence into 300-d vector
class PhraseVector:
    def __init__(self, phrase):
        self.vector = self.PhraseToVec(phrase)
        
    def ConvertVectorSetToVecAverageBased(self, vectorSet, ignore = []):
        if len(ignore) == 0: 
            return np.mean(vectorSet, axis = 0)
        else: 
            return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)

    def PhraseToVec(self, phrase):
        cachedStopWords = stopwords.words("english")
        phrase = phrase.lower()
        wordsInPhrase = [word for word in phrase.split() if word not in cachedStopWords]
        vectorSet = []
        for aWord in wordsInPhrase:
            try:
                wordVector=model1[aWord]
                vectorSet.append(wordVector)
            except:
                pass
        return self.ConvertVectorSetToVecAverageBased(vectorSet)
    
    # Cosine Similarity to determine how close two questions are
    def CosineSimilarity(self, otherPhraseVec):
        cosine_similarity = np.dot(self.vector, otherPhraseVec) / (np.linalg.norm(self.vector) * np.linalg.norm(otherPhraseVec))
        try:
            if math.isnan(cosine_similarity):
                cosine_similarity=0
        except:
            cosine_similarity=0
        return cosine_similarity


# In[30]:


class EasyReply():
    def __init__(self, faq_qna):
        self.name = 'Robot'
        self.faq_qna = faq_qna
    # Get closest FAQ question based on input  
    def answer(self, text, question=False):
        qn_df = self.faq_qna.copy()
        text_qn = PhraseVector(text)
        qn_df['scoring'] = [text_qn.CosineSimilarity(PhraseVector(qn).vector) for qn in qn_df['FAQ Question']]
        max_row = qn_df.sort_values(by=['scoring'], ascending=False).iloc[0,:]
        if question:
            return max_row['FAQ Question']
        return max_row['FAQ Answer']
        
        
        
    def evalData(self, input_qns, actual_match_qns):
        y_pred_class = [self.answer(qn, True) for qn in input_qns]
        print('Accuracy: ', metrics.accuracy_score(actual_match_qns, y_pred_class))
        return pd.DataFrame({'Input':input_qns, 'Output':y_pred_class,'Actual':actual_match_qns})


# In[31]:


# test_data = pd.read_csv('test_data.csv')
# train_data = pd.read_csv('singtel_qna.csv',header=None)
# train_data.columns = ['Question','Answer']


# faq_qns = pd.DataFrame({'FAQ Question':train_data['Question'], 'FAQ Answer':train_data['Answer']})
# er = EasyReply(faq_qns)
# X = test_data['Questions']
# y = test_data['FAQ Question']


# # In[32]:


# qn = 'Why does my internet connection keeps disconnecting?'
# print(er.answer(qn))


# # In[33]:


# # evaluate matrix
# er.evalData(X,y)


# In[ ]:




