import requests
from bs4 import BeautifulSoup

questions = []
answers = []

googled_urls = ['https://www.singtel.com/personal/i/internet/broadband-at-home/faqs',
        'https://www.singtel.com/personal/i/faq/mobileShareFaqs',
        'https://www.singtel.com/personal/i/phones-plans/mobile/vas/datamore/faq',
        'https://www.singtel.com/personal/i/internet/home-broadband/fibre-broadband-0/faqs/faq-0']

for url in googled_urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    questions_soup = soup.find_all(['div','li'], class_ = 'qna-item')
    for q in questions_soup:
        questions.append(q.h6.text)
        answers.append(q.div.text)

'''support_urls = ['https://www.singtel.com/personal/support/account-billing',
        'https://www.singtel.com/personal/support/mobile-postpaid',
        'https://www.singtel.com/personal/support/prepaid-cards',
        'https://www.singtel.com/personal/support/broadband',
        'https://www.singtel.com/personal/support/singtel-tv',
        'https://www.singtel.com/personal/support/telephony',
        'https://www.singtel.com/personal/support/online-purchases',
        'https://www.singtel.com/personal/support/lifestyle']'''


with open('qna.csv','w', encoding='utf-8') as file:
    for question,answer in zip(questions,answers):
        question = question.replace(',','').strip()
        answer = answer.replace(',','').strip()
        file.write(question.replace('\n','') + ',' + answer.replace('\n',''))
        file.write('\n')
file.close()