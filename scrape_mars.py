from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt

executable_path = {'executable_path': '/usr/lib/chromium-browser/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape_site():
    news_title, news_body = mars_news(browser)
    results = {
        "title": news_title,
        "body": news_body,
        "image_URL": space_images(browser),
        "weather": mars_weather(browser),
        "facts": mars_facts(browser),
        "hemispheres": mars_hemispheres(browser),
    }

    browser.quit()
    return results


def mars_news(browser):
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = bs(html,"html.parser")

    try:
        news_title = soup.find("div",class_="content_title").get_text()
        news_body = soup.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None



def space_images(browser):
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    html = browser.html
    soup = bs(html, "html.parser")
    img = soup.find("img", class_="thumb")["src"]
    img_url = "https://www.jpl.nasa.gov" + img
    return(img_url)


def mars_weather(browser):
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    html = browser.html
    soup = bs(html,"html.parser")
    try:
        weather_tweet =soup.find('p', class_='TweetTextSize').get_text()
    except AttributeError:
        return None, None


def mars_facts(browser):
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html
    soup = bs(html,"html.parser")

    tables = pd.read_html(facts_url)
    df = tables[1]
    df.columns = ['1','2','3']
    return(df.to_html())


def mars_hemispheres(browser):
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html,"html.parser")

    mars_hemispheres_strings = []
    links = soup.find_all('h3')

    for hemispheres in links:
        mars_hemispheres_strings.append(hemispheres.text)

    hemisphere_image_urls = []
    for hemispheres in mars_hemispheres_strings:
        hemispheres_dict = {}
        browser.click_link_by_partial_text(hemispheres)
        hemispheres_dict["img_url"] = browser.find_by_text('Sample')['href']
        hemispheres_dict["title"] = hemispheres
        hemisphere_image_urls.append(hemispheres_dict)
        browser.back()

    print(hemisphere_image_urls)
    return hemisphere_image_urls



if __name__=="__main__":
    print(scrape_site())