import requests
from bs4 import BeautifulSoup

questions = []
answers = []

fibre_page = requests.get('https://www.singtel.com/personal/i/internet/broadband-at-home/faqs')
soup = BeautifulSoup(fibre_page.text, 'html.parser')
questions_soup = soup.find_all('li', class_ = 'qna-item')
for q in questions_soup:
    questions.append(q.h6.text)
    answers.append(q.div.text)

mobishare_page = requests.get('https://www.singtel.com/personal/i/faq/mobileShareFaqs')
soup = BeautifulSoup(mobishare_page.text, 'html.parser')
questions_soup = soup.find_all('div', class_ = 'qna-item')
for q in questions_soup:
    questions.append(q.h6.text)
    answers.append(q.div.text)

datamore_page = requests.get('https://www.singtel.com/personal/i/phones-plans/mobile/vas/datamore/faq')
soup = BeautifulSoup(datamore_page.text, 'html.parser')
questions_soup = soup.find_all('div', class_ = 'qna-item')
for q in questions_soup:
    questions.append(q.h6.text)
    answers.append(q.div.text)

with open('qna.csv','w') as file:
    for question,answer in zip(questions,answers):
        question = question.replace(',','').strip()
        answer = answer.replace(',','').strip()
        file.write(question.replace('\n','') + ',' + answer.replace('\n',''))
        file.write('\n')

file.close()