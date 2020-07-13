import time
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #visit url
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html

    #parse html
    soup = bs(html, "html.parser")

    #find title and body
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_body = article.find("div", class_="article_teaser_body").text

    #visit url for images
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    soup = bs(html, "html.parser")

    # Get images
    feat_img_url = soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'

    #scrape tweets
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    tweet_container = soup.find_all('div', class_="js-tweet-text-container")

    for tweet in tweet_container:
        mars_weather = tweet.find('p').text
        if 'sol' and 'pressure' in mars_weather:
            break
        else:
            pass


    #mars facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    table = pd.read_html(facts_url)
    mars_facts = table[1]
    mars_facts.columns = ['Description', 'Value']
    mars_facts = mars_facts.set_index('Description')
    mars_facts = mars_facts.to_html(classes="table table-striped")

    #mars hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_urls = []
    results = soup.find("div", class_="result-list")
    hemispheres = results.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_urls.append({"title": title, "img_url": image_url})


    mars_data = {
        "news_title": news_title,
        "news_p": news_body,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_urls
    }

    browser.quit()
    return mars_data

if __name__ == '__main__':
    scrape()