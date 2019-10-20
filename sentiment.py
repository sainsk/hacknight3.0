import csv
import time
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
import sys

def execute(news):
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome("chromedriver.exe", chrome_options=options)

    browser.maximize_window()
    browser.get('https://developer.aylien.com/text-api-demo?text=Literally%20ur%20facebook%20message%20app%20is%20useless%2C%20you%20only%20want%20it%20to%20increase%20profit.%20Please%20fix%20yourself.%20Its%20sad%20%40facebook&tab=sentiment&run=1')

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[1]/label/textarea').clear()

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[1]/label/textarea').send_keys(news)
    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[2]/label/div/input').click()

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[2]/label/div/div/div[1]').click()

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[3]/label/div/input').click()

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[1]/div/div[3]/label/div/div/div[1]').click()

    browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[1]/div[2]/form/div[2]/button').click()
    time.sleep(5)
    polarity = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td[1]').text
    confidence = browser.find_element_by_xpath(
        '//*[@id="root"]/div/div/div/div[2]/div/div[3]/div/div[2]/div/div[2]/div/div[3]/table/tbody/tr/td[2]').text

    return [polarity, confidence]

def smsMethod(cmp,sentiment,contact):
   API_ENDPOINT = "https://alerts.solutionsinfini.com//api/v4/index.php"
   data = {'method': 'sms',
       'message': "News Feed on Your Stock\n"+cmp+"\nPolarity - {}\nConfidence - {}".format(sentiment[0],sentiment[1]),
       'sender': 'HACKAT',
       'api_key': 'A91862b9c45ff3872032bb46332b1be86',
       'to': contact}
   r = requests.post(url=API_ENDPOINT, data=data)
   print(r.status_code)

# from pattern.en import ngrams
Base_url = "http://www.moneycontrol.com"
# Build a dictionary of companies and their abbreviated names
companies = {'HDFC': 'HDF01'}
# data = requests.get(url = "http://virtual.cmuvefdf4m.ap-south-1.elasticbeanstalk.com/stockurl/")
# for stock_data in data.json()["data"]:
#     name = stock_data['name']
#     url = stock_data['url']
#     new_key_value = url.split("/")
#     key = new_key_value[-2]
#     value = new_key_value[-1]
#     companies[key] = value
# Create a list of the news section urls of the respective companies
url_list = ['http://www.moneycontrol.com/company-article/{}/news/{}#{}'.format(
    k, companies[k], companies[k]) for k in companies]
List_of_links = []
# 'http://www.moneycontrol.com/company-article/HDFC/news/HDF01#HDF01'
# Extract the relevant news articles weblinks from the news section of selected companies
for urls in url_list:
    html = requests.get(urls)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html.text, 'html.parser')
    sub_links = soup.find_all('a', class_='arial11_summ')
    for links in sub_links:
        # first convert into a string
        sp = BeautifulSoup(str(links), 'html.parser')
        tag = sp.a
        category_links = Base_url + tag["href"]
        List_of_links.append(category_links)
        # print(category_links)
# unique_links = list(set(List_of_links))
unique_links = List_of_links[:1]
for selected_links in unique_links[:1]:
    results_url = selected_links
    print(results_url)
    results = requests.get(results_url)
    raw_result = results.text.split('<script type="application/ld+json">')
    new_raw_result = []
    for x in raw_result[1:len(raw_result)-1]:
        new_raw_result.append(x.split("</script>")[0])
    for data in new_raw_result:
        if "articleBody" in data:
            rev = data[::-1]
            filter_data = data[data.index(
                "[")+1:(len(data)-rev.index("]"))-1].replace("\n", " ").replace('\r', '')
            extract_text = json.loads(filter_data)
            final_text = extract_text["articleBody"]
            date = extract_text["dateModified"]
            dataset = execute(final_text)
            print(dataset)
            smsMethod(results_url,dataset,int(sys.argv[1]))
