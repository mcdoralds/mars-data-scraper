#!/usr/bin/env python
# coding: utf-8

# In[59]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager


# In[60]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[61]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[62]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[63]:


slide_elem.find('div', class_='content_title')


# In[64]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[65]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# In[66]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[67]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[68]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[69]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[70]:


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

# In[71]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


# In[72]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[73]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[74]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[75]:


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
    img_temp = soup(html, 'html.parser') # use bs4 to extract image
    title = img_temp.find('h2').text # extract image title
    
    try:
        full_image = browser.find_by_css('#wide-image > div > ul > li:nth-child(1) > a').first
        hemisphere_image_urls.append({"image_url": full_image['href'], "title":title})
        print(full_image['href'])
        browser.back()
        
    except Exception as e :
        print(e)


# In[76]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[77]:


# 5. Quit the browser
browser.quit()


# In[ ]:




