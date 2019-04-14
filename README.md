# FAQ Chatbot

Don't have a chatbot on your website or Facebook page yet? Underutilized FAQ? 
Try bringing your FAQ to life using this chatbot!

## Getting Started

These instructions will get you setup with the required tools and packages to run on your local system.

### Prerequisites

Python 3.x Packages

```python
nltk
pandas
sklearn
scipy
numpy
flask
flask_restful
bs4
selenium
```

Additional Files

```bash
# Chrome Driver
chromedriver.exe (or any preferred driver)

# Google News Vector
wget -c "https://s3.amazonaws.com/dl4j-distribution/GoogleNews-vectors-negative300.bin.gz"
```

### Installing

There are 3 main steps required to get the chatbot up and running:
1) Scraping of FAQ page
2) Scraping of Facebook page<br>_(Only used to determine % of Facebook posts can be answered by FAQ, otherwise not necessary)._
3) Building the Model

**Step 1: Scraping of FAQ page**

Ensure that chromedriver.exe is in the same directory as company_scraper.py. Edit company_scraper.py as such:

```python
if __name__ == '__main__':
  soup_urls = ['link here']
  scrape('output_csv_filename.csv', soup_urls')
```
Run the script and a csv file containing the Questions and Answers should be saved in the same directory.
```python
python company_scraper.py
```

**Step 2: Scraping of Facebook page**

Ensure that you have configured config_fb_cred.json to contain your login credentials.

```json
{
	"email":"Facebook Account Email",
	"password":"Facebook Account PW"
}
```

Insert the facebook url in facebook_scraper.py. The facebook posts will be saved as [company]_fb_questions.csv.

```python
if __name__ == "__main__":
	url = 'https://www.facebook.com/<company fb user>/posts_to_page/'
	loopCount = 2 # <- Change loop count if you want more posts to be scraped
scrapePost(url, loopCount)
```

**Step 3: Building the Model**

Edit app.py to import the CSVs you have just scraped.

```python
er = EasyReply
train_data = pd.read_csv('singtel_qna.csv',header=None) #<- Change this to your csv file name
train_data.columns = ['Question','Answer']
faq_qns = pd.DataFrame({'FAQ Question':train_data['Question'], 'FAQ Answer':train_data['Answer']})
er = EasyReply(faq_qns)
```

Next, if running the app on localhost, change to the following. Otherwise for production, leave it.

```python
if __name__ == '__main__':
     # For actual
     # app.run(host="0.0.0.0")
    app.run()
```

Now, you can go to your browser and type the following: localhost/question/&lt;insert your question here&gt;. The app will return a JSON response with the answer from FAQ.

## Model Exploratory Process

Code developed during exploratory process to compare models can be found under `"Model Exploration.ipynb"` / `"Model Exploration.html"`.

## Deployment

Connect your bot, e.g. DialogFlow, to send a GET request to &lt;your machine ip address&gt;/question/&lt;user message&gt; and return the answer section of the JSON response.

## Acknowledgments

* Prof Zhao Yiliang for BT4222 class and sharing invaluable knowledge.

