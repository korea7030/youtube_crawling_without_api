from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import re

def get_urls_from_youtube_with_keyword(keyword):
    titles = []
    urls = []

    search_keyword_encode = requests.utils.quote(keyword)

    url = 'https://www.youtube.com/results?search_query=' + search_keyword_encode

    driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')

    driver.get(url)

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        time.sleep(3.0)
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        time.sleep(3.0)

        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            break
        
        last_page_height = new_page_height
    
    html_source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html_source, 'lxml')

    datas = soup.select('a#video-title')

    for data in datas:
        title = data.text.replace('\n', '')
        url = "https://www.youtube.com/" + data.get('href')

        titles.append(title)
        urls.append(url)
    
    return titles, urls

def crawl_youtube_page_html_sources(urls):
    html_sources = []

    for url in urls:
        driver = wd.Chrome(executable_path='/usr/local/bin/chromedriver')
        driver.get(url)

        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            time.sleep(2.0)
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            time.sleep(3.0)
            new_page_height = driver.execute_script('return document.documentElement.scrollHeight')

            if new_page_height == last_page_height:
                break
            last_page_height = new_page_height
        html_source = driver.page_source
        html_sources.append(html_source)
        print('OK')

        driver.quit()
    return html_sources