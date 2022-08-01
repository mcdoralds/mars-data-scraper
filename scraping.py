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

    news_title, news_paragraph = mars_news(browser) # set variables

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres":hemispheres(browser)
    }

    # Stop webdriver and return data
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
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html(classes="table table-striped") # convert dataframe into HTML format and add bootstrap


# D2: Scrape High-Resolution Mars’ Hemisphere Images and Titles
def hemispheres(browser):
    # Hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    hemispheres = soup(browser.html, 'html.parser')
    images = hemispheres.find_all('a', class_ = 'itemLink product-item') # define image to be extracted from site
    images_set = list(set([image['href'] for image in images if image['href'].find('#')== -1])) # save images

    print(images_set)

    for image_url in images_set: # will loop through the tags
        hemispheres = {} # create an empty dictionary
        
        base_image_urls = f'{url}{image_url}' # format for URLs that will be stored as strings
        browser.visit(base_image_urls) # use splinter to visit image
        img_temp = soup(browser.html, 'html.parser') # use bs4 to extract image
        title = img_temp.find('h2').text # extract image title
        
        try:
            full_image = browser.find_by_css('#wide-image > div > ul > li:nth-child(1) > a').first
            hemisphere_image_urls.append({"image_url": full_image['href'], "title":title})
            print(full_image['href'])
            browser.back()
            
        except Exception as e :
            print(e)


    return hemisphere_image_urls


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())