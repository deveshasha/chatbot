
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json
import pandas as pd
import sys
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

credentials = 'config_fb_cred.json'
# credentials = 'config_fb.json'
with open(credentials) as json_data_file:
    token_file = json.load(json_data_file)

# Authentication
email_id = token_file['email']
if email_id == "Facebook Account Email":
	print('Error: Please ensure that you entered your Facebook Account Credentials in config_fb_cred.json file.')
	sys.exit()
password = token_file['password']

#Parameters
total_scrolls = 5000
current_scrolls = 0
scroll_time = 5
stop_date = datetime(year=2017, month=12, day=1)

def extractPost(post):
    date = post.find_element

def getPostText(webelement):
    try:
        post_text = webelement.find_element_by_css_selector('p').text
    except:
        post_text = None
    try:
        comment = webelement.find_element_by_css_selector('._ipm._-56')
        if comment:
            link = comment.get_attribute("href")
#     date_text = webelement.find_element_by_css_selector('.fsm.fwn.fcg').text
#     dt = datetime.strptime(date_text, '%B %d, %Y')
    except:
        link = None
#     print(link)
#     print(post_text)
    return post_text, link

def scrapePost(fbpage, loopCount):
    
    def check_height():
        new_height = driver.execute_script("return document.body.scrollHeight")
        return new_height != old_height

    def scroll():
        global old_height
        current_scrolls = 0

        while (True):
            try:
                if current_scrolls == total_scrolls:
                    return

                old_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                WebDriverWait(driver, scroll_time, 0.05).until(lambda driver: check_height())
                current_scrolls += 1
            except TimeoutException:
                break

        return

    
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.facebook.com/')
    print("Opened facebook...")
    a = driver.find_element_by_id('email')
    a.send_keys(email_id)
    print("Email Id entered...")
    b = driver.find_element_by_id('pass')
    b.send_keys(password)
    print("Password entered...")
    c = driver.find_element_by_id('loginbutton')
    c.click()

    #Open target page
    driver.get(fbpage)
    company = fbpage.split('/')[-3]
    all_posts = []
    post_count = []
    delay = 5
    big_pic = driver.find_element_by_css_selector("._4t2a")
    # Set number of times to loop
    for i in range(0,loopCount):
        print('Loop', i)
        try:
            elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.LINK_TEXT, 'See More Posts')))
            elem.click()
        except:
            print('error but it is fine')
        scroll()
        print('Scrolling...')
        time.sleep(3)
    all_posts = big_pic.find_elements_by_css_selector("._5pcr.userContentWrapper")


    df_text = []
    df_comments = []
    for post in all_posts:
        txt, comment = getPostText(post)
        df_text.append(txt)
        df_comments.append(comment)
    df = pd.DataFrame({'post_text':df_text,'post_comment':df_comments})
    print('Saved to CSV')
    df.to_csv(company + '_fb_questions.csv',index=False)

if __name__ == "__main__":
	#Change here
	url = 'https://www.facebook.com/singtel/posts_to_page/'
	loopCount = 10
	scrapePost(url, loopCount)

