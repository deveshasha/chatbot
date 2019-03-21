import requests
from bs4 import BeautifulSoup
from selenium import webdriver

questions = []
answers = []

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.implicitly_wait(50)

soup_urls = ['https://www.singtel.com/personal/i/internet/broadband-at-home/faqs',
        'https://www.singtel.com/personal/i/faq/mobileShareFaqs',
        'https://www.singtel.com/personal/i/phones-plans/mobile/vas/datamore/faq',
        'https://www.singtel.com/personal/i/internet/home-broadband/fibre-broadband-0/faqs/faq-0']

for url in soup_urls:
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	questions_soup = soup.find_all(['div','li'], class_ = 'qna-item')
	for q in questions_soup:
		questions.append(q.h6.text)
		answers.append(q.div.text)

selenium_urls = ['https://www.singtel.com/personal/support/account-billing',
        'https://www.singtel.com/personal/support/mobile-postpaid',
        'https://www.singtel.com/personal/support/prepaid-cards',
        'https://www.singtel.com/personal/support/broadband',
        'https://www.singtel.com/personal/support/singtel-tv',
        'https://www.singtel.com/personal/support/telephony',
        'https://www.singtel.com/personal/support/online-purchases',
        'https://www.singtel.com/personal/support/lifestyle/connectedthings',
        'https://www.singtel.com/personal/support/lifestyle/Oaxis',
        'https://www.singtel.com/personal/support/lifestyle/trackimo']

for url in selenium_urls:
	driver.get(url)
	soup = BeautifulSoup(driver.page_source, 'html.parser')
	questions_soup = soup.find_all('a', class_ = 'faq-que-link' )
	answers_soup = soup.find_all('div', class_ = 'faq-ans-desc')
	for q, a in zip(questions_soup, answers_soup):
		questions.append(q.text)
		answers.append(a.text)

selenium_urls_2 = ['https://www.singtel.com/personal/support/broadband/troubleshoot',
                   'https://www.singtel.com/personal/support/telephony/troubleshoot',
                   'https://www.singtel.com/personal/support/singtel-tv/troubleshoot']
for url in selenium_urls_2:
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for text in soup.find_all('div', class_=' description-text body-copy-text v-none-top'):
        for a in text.find_all('a', href=True):
            questions.append(a.text)
            answers.append('Please follow the instructions given here: https://www.singtel.com' + a['href'])
		

driver.close()

with open('qna.csv','w', encoding='utf-8') as file:
    for question,answer in zip(questions,answers):
        question = question.replace(',','').strip()
        answer = answer.replace(',','').strip()
        file.write(question.replace('\n',' ') + ',' + answer.replace('\n',' '))
        file.write('\n')
file.close()
