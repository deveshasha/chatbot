import pandas as pd
import nltk
from nltk.corpus import stopwords
import gensim
from gensim.models import Word2Vec
# import pyemd
model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
model_n = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True) 
model_n.init_sims(replace=True) #normalized

#Read data
qna = pd.read_csv('qna.csv', error_bad_lines=False)
fb = pd.read_csv('singtel_fb_questions.csv', error_bad_lines=False)
qna.columns = ['question']

#Obtain index of the final question in Q and A as well as in the Facebook posts that we scraped:
last_qna = qna.tail(1).index.item()
last_fb = fb.tail(1).index.item()

n = 0 #numerator +=1 if we determine that the fb question can be answered by one of the faq question
d = 0 #denominator +=1 every iteration

for i in range(0,last_fb+1):
    question1 = fb.post_text[i]
  
    if isinstance(question1,str):
    
        if '?' in question1:
            question1 = question1.lower().split()
            question1 = [w for w in question1 if w not in stopwords.words('english')]

            for j in range(0,last_qna+1):
                question2 = qna.iloc[j,0]
                question2 = question2.lower().split()
                question2 = [w for w in question2 if w not in stopwords.words('english')]

                distance = model.wmdistance(question1, question2)
                distance_n = model_n.wmdistance(question1, question2)

                if (abs(distance-distance_n) > 3):
                    n += 1
                    break
      
            d += 1
  
print(n/d)
