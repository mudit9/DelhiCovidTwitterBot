import sys
import tweepy
import requests
from datetime import date, timedelta
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver

from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

if __name__ == '__main__':

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # Create API object

    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print('Authentication Successful')
    except:
        print('Error while authenticating API')
        sys.exit(1)

    my_url = "https://www.mygov.in/covid-19"
    driver = webdriver.Chrome()
    driver.get(my_url)
    driver.find_elements_by_class_name("plus_icon")[1].click()
    maintable = driver.find_element_by_id("_indiatable")
    table1 = maintable.find_element_by_id("ind_mp_tbl")
    table2 = table1.find_element_by_css_selector("tbody")
    tablerow = table2.find_elements_by_css_selector("tr")
    indx = 100000
    for i,row in enumerate(tablerow):
        print(row.find_elements_by_css_selector("td")[0].text.strip())
        if row.find_elements_by_css_selector("td")[0].text.strip() == "Delhi":
            indx = i
            break
    tablerow = tablerow[indx]
    mainTxt = tablerow.find_elements_by_class_name("data-up")
    daily_cases = mainTxt[0].text
    #print("Daily cases: ",daily_cases)
    today = date.today()
    yesterday = today - timedelta(days = 1)
    tweet = str(yesterday) + "\n" + "Daily Covid-19 cases in New Delhi:\n"+ daily_cases
    api.update_status(tweet)
    print("tweeted \n",tweet)
