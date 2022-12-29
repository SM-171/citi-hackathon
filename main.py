import streamlit as st
import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date

months = {"01":"January",
          "02":"February",
          "03":"March",
          "04":"April",
          "05":"May",
          "06":"June",
          "07":"July",
          "08":"August",
          "09":"September",
          "10":"october",
          "11":"November",
          "12":"December"}

def get_date():
    today = str(date.today()).split('-')
    dd = today[2]
    mm = months[today[1]]
    yy = today[0]
    
    return dd + " " + mm + ", " + yy

def filter_todays_headlines(headlines):
    return {key:value for (key, value) in headlines.items() if value['date'] == str(date.today())}

def extract_headlines(news):
    headlines = {}
    for article in news:
        headline = str(article.find('a').text.strip())
        if headline != "":
            headlines[headline] = {}
            headlines[headline]['link'] = "https://www.business-standard.com"+str(article.find('a')['href'].strip())
    
    for headline in headlines:
        # print(headlines[headline]['link'])
        article_page = requests.get(headlines[headline]['link'])
        article_text = BeautifulSoup(article_page.text, "html.parser")
        
        author_info = article_text.find('p', attrs={'class':'authorTxt'})
        headlines[headline]["author_name"] = str(author_info.find('a').text.strip())
        headlines[headline]["date"] = author_info.find('span', attrs = {'itemprop':'datePublished'})['content']

    return headlines


def get_news():
    URL = "https://wap.business-standard.com/markets-news"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    news = soup.find_all('div', attrs={'class':'article'})

    todays_headlines = filter_todays_headlines(extract_headlines(news))
    # print(todays_headlines)

    st.subheader('Latest NSE News')
    st.caption('Date: ' + get_date())

    i = 1
    for headline in todays_headlines:
        st.markdown(str(i) + ") " + headline + ".")
        st.markdown("[[Article Link]](todays_headlines[headline]['link'])  |  Author: " + todays_headlines[headline]['author_name'])
        i += 1

get_news()