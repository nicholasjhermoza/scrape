from splinter import Browser
from bs4 import BeautifulSoup
import time
import re
import requests as req
from splinter import Browser


def scrape():
    mars_dict = {}
    #Navigation
    executable_path = {'executable_path' : '/Users/nicho/Downloads/chromedriver_win32/chromedriver'}
    browser = Browser("chrome", **executable_path, headless = True)
  
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    title_path = news_soup.select_one('ul.item_list li.slide')
    news_title = title_path.find('div', class_='content_title').text
    news_p = title_path.find('div', class_='article_teaser_body').get_text()
    #assign to dictionary
    mars_dict["news_title"]=news_title
    mars_dict["news_p"]=news_p

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text("FULL IMAGE")
    time.sleep(3)
    browser.click_link_by_partial_text("more info")
    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image_url = soup.find('figure', class_='lede')
    image_link = image_url.a["href"]
    feature_image_url = "https://www.jpl.nasa.gov" + image_link
    
    mars_dict["feature_image_url"]=feature_image_url

       
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(3)
    html = browser.html
    soup1 = BeautifulSoup(html, "html.parser")
    m_weather_tweet = soup1.find('div', attrs={"class": "tweet", "data-name": "Mars Weather"})

    try:
        m_weather = m_weather_tweet.find("p", "tweet-text").get_text()
        m_weather
    except AttributeError:
        pattern = re.compile(r'sol')
        m_weather = soup1.find('span', text=pattern).text
        m_weather
    m_weather

    mars_dict["m_weather"]=m_weather

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

    mars_dict["mars_hemisphere"]=mars_hemisphere

    return mars_dict

