# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)   

    # Set variables
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

# stop webdriver and return data
browser.quit()
return data




def mars_news(browser):

    # Visit the Mars news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Searching for elements with div and list_text tags
    browser.is_element_present_by_css('div.list_text', wait_time = 1) # optional delay for loading the page

    # Convert to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try: # add try/except for error handling
        slide_elem = news_soup.select_one('div.list_text') 
        # Use parent element to find the first <a> tag and save it as "news_title"
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
    return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
    return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
    # use .read_html() to scrape the facts table into a pandas dataframe
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
    return None

    # assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html() # convert dataframe into HTML format and add bootstrap


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())