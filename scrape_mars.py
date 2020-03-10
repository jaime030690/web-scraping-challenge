# Dependencies
import pandas as pd
from bs4 import BeautifulSoup
from splinter.browser import Browser
import requests
from pprint import pprint

# Selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Sprinter
from splinter import Browser

def scrape():

    '''

    Scrape Mars News
    
    '''
    url = "https://mars.nasa.gov/news/"

    driver = webdriver.Chrome()
    driver.get(url)
    timeout = 3

    # Find first title
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    news_title = soup.find('div', class_="content_title").find('a').text

    # Find first teaser
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'article_teaser_body'))
        news_p = WebDriverWait(driver, timeout).until(element_present).text
    except TimeoutException:
        print("Timed out waiting for page to load")

    # Close Chrome driver
    driver.quit()

    '''

    Featured Image

    '''

    # Setup sprinter object
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Open Chrome with browser for scrape
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')
    browser.click_link_by_partial_text("more info")

    # BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    featured_image_url = "https://www.jpl.nasa.gov" + soup.find('img', class_="main_image")['src']

    # Close browser
    browser.quit()

    '''

    Mars Weather / Twitter

    url = 'https://twitter.com/MarsWxReport?lang=en'

    driver = webdriver.Chrome()
    driver.get(url)
    timeout = 3

    # Find weather element
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'css-16my406'))
        weather = WebDriverWait(driver, timeout).until(element_present).text
    except TimeoutException:
        print("Timed out waiting for page to load")

    # Close Chrome driver
    driver.quit()
    
    '''
    '''

    Mars Facts

    '''

    # Load Mars Facts table
    facts_table = pd.read_html("https://space-facts.com/mars/")[0]
    facts_str = facts_table.to_html()

    '''
    
     Mars Hemispheres

    '''

    # Setup sprinter object
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": ""},
        {"title": "Cerberus Hemisphere", "img_url": ""},
        {"title": "Schiaparelli Hemisphere", "img_url": ""},
        {"title": "Syrtis Major Hemisphere", "img_url": ""},
    ]

    # Open Chrome with browser for scrape
    browser.visit(url)

    for hemisphere in hemisphere_image_urls:
        browser.click_link_by_partial_text(hemisphere['title'])
        html = browser.html
        soup = BeautifulSoup(html, 'lxml')
        url = soup.find('div', class_='downloads').find('li').find('a')['href']
        hemisphere.update(img_url = url)
        browser.back()

    browser.quit()

    '''

    Return dict

    '''

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": '',
        "facts_str": facts_str,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data

