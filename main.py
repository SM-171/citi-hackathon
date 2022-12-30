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
            # print(headline)
    
    for headline in headlines:
        # print(headlines[headline]['link'])
        article_page = requests.get(headlines[headline]['link'])
        article_text = BeautifulSoup(article_page.text, "html.parser")
        
        author_info = article_text.find('p', attrs={'class':'authorTxt'})
        # print(author_info)
        if(author_info != None):
            headlines[headline]["author_name"] = str(author_info.find('a').text.strip())
            headlines[headline]["date"] = author_info.find('span', attrs = {'itemprop':'datePublished'})['content']
        else:
            # print(headlines[headline]['link'])
            headlines[headline]["author_name"] = "Anonymous Source"
            headlines[headline]["date"] = str(date.today())

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
def get_top_surfers():
    #top 5 gainers
    st.header("Top Gainers for NSE")
    df = pd.read_html("https://www.way2wealth.com/market/indicestopgainers/")
    st.table(df[123].head(5))

    #top 5 losers
    st.header("Top Losers for NSE")
    df = pd.read_html("https://www.way2wealth.com/market/indicestoplosers/")
    st.table(df[123].head(5))
   
def get_market_turnover():
    #print market turnover
    df = pd.read_html("https://www.way2wealth.com/market/volumeturnover/")
    df= df[123].head(1)
    df.drop(['Date'], axis=1, inplace= True)
    st.header("Market Turnover")
    st.table(df)


st.markdown('<div style="text-align: center; font-size: 3rem; font-weight: bolder; ">Market Commentary</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 1rem; text-decoration: underline;">Intended for Institutional Clients Only</div>', unsafe_allow_html=True)
get_news()
get_top_surfers()
get_market_turnover()