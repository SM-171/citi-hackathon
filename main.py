import streamlit as st
import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import date, timedelta

months = ["", "January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]

#convert date to dd/mm/yy format
def get_date():
    today = str(date.today()).split('-')
    dd = today[2]
    mm = months[int(today[1])]
    yy = today[0]

    return dd + " " + mm + ", " + yy


#filter latest headlines published today and the previous day
def filter_todays_headlines(headlines):
    today = date.today()
    return {key:value for (key, value) in headlines.items() if value['date'] == str(today) or value['date'] == str(today - timedelta(days = 1)) }


#utility function for get_news() function
#to extract relevant highlights related to the stock market
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


#to find and display relevant highlights on the report
def get_news():
    URL = "https://wap.business-standard.com/markets-news"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, "html.parser")

    news = soup.find_all('div', attrs={'class':'article'})

    todays_headlines = filter_todays_headlines(extract_headlines(news))

    st.subheader('NSE Highlights')

    i = 1
    for headline in todays_headlines:
        st.markdown(str(i) + ") " + headline + ".\n")
        st.markdown("🔗" + "[[Article Link]]({})".format(todays_headlines[headline]['link']) + "  |  Author : " + todays_headlines[headline]['author_name'])
        i += 1
    
    st.markdown("---")


#ultility function for get_trends() function
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


#to get the trending keywords for stock market SEOs
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

    # st.markdown("---")


#to find the top surfers in the stock market on a given day
def get_top_surfers():
    #top 5 gainers
    st.subheader("Top Gainers for NSE")
    df = pd.read_html("https://www.way2wealth.com/market/indicestopgainers/", match="Total Traded Value")
    df[0].drop(['Exchange Group'], axis=1, inplace=True)
    st.table(df[0].head(5))
    st.caption("NOTE: All trade values are in INR(Indian Rupees)")
    st.markdown("---")

    #top 5 losers
    st.subheader("Top Losers for NSE")
    df = pd.read_html("https://www.way2wealth.com/market/indicestoplosers/", match="Total Traded Value")
    df[0].drop(['Exchange Group'], axis=1, inplace=True)
    st.table(df[0].head(5))
    st.caption("NOTE: All trade values are in INR(Indian Rupees)")
    st.markdown("---")


#to get the market turnover
def get_market_turnover():
    #print market turnover
    df = pd.read_html("https://www.way2wealth.com/market/volumeturnover/", match="Turnover")
    df= df[0].head(1)
    df.drop(['Date'], axis=1, inplace= True)
    st.subheader("Market Turnover (NSE)")
    st.table(df)
    st.caption("NOTE: All trade values are in INR(Indian Rupees)")
    st.markdown("---")

def get_adr_gdr_prices():
    st.subheader("ADR GDR Prices")
    df = pd.read_html("https://www.way2wealth.com/market/adrgdr/", match="Volume")
    #df[0].drop(['Exchange Group'], axis=1, inplace=True)
    st.table(df[0].head(5))
    st.caption("NOTE: All trade values are in INR(Indian Rupees)")
    st.markdown("---")

def main():
    st.markdown('<div style="text-align: center; font-size: 3rem; font-weight: bolder; ">Market Commentary</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1rem; color: grey">[Intended for Institutional Clients Only]</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; font-size: 1.2rem; font-weight: bolder;">Date: {}</div>'.format(get_date()), unsafe_allow_html=True)
    st.markdown("---")

    get_news()
    get_top_surfers()
    get_market_turnover()
    get_adr_gdr_prices()
    get_trends()


if __name__ == "__main__":
    main()