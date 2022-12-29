import streamlit as st
import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta
from prettytable import PrettyTable

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
    today = date.today()
    return {key:value for (key, value) in headlines.items() if value['date'] == str(today) or value['date'] == str(today - timedelta(days = 1)) }

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

    st.header('NSE Highlights')
    st.caption('Date: ' + get_date())

    i = 1
    for headline in todays_headlines:
        st.markdown(str(i) + ") " + headline + ".\n")
        st.markdown("🔗" + "[[Article Link]]({}))".format(todays_headlines[headline]['link']) + "  |  Author : " + todays_headlines[headline]['author_name'])
        i += 1
    
    st.markdown("---")
    get_trends()

def find_trending_words():
    url = "https://economictimes.indiatimes.com/marketstats/pid-40,exchange-nse,sortby-value,sortorder-desc.cms"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    trending = soup.find('div', attrs={'class':'seoWidget_con'})
    trending_market = trending.find_all('a')

    trending_words = []
    for trends in trending_market:
        trending_words.append(trends.text) 
        # = "https://economictimes.indiatimes.com"+trends['href']

    return trending_words

def get_trends():
    st.subheader("Trending in Market")
    words = find_trending_words()

    col1, col2, col3, col4  = st.columns(4)

    i = 0
    while i < len(words):
        with col1:
            st.button(words[i])
            i += 1

        if(i == len(words)):
            break

        with col2:
            st.button(words[i])
            i += 1
        
        if(i == len(words)):
            break
    
        with col3:
            st.button(words[i])
            i += 1
        
        if(i == len(words)):
            break
        
        with col4:
            st.button(words[i])
            i += 1

get_news()