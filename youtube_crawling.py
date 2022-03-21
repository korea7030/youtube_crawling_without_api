from selenium import webdriver as wd
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import json

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
        href = data.get('href')
       
        if 'shorts' not in href:
            title = data.text.replace('\n', '')
            url = "https://www.youtube.com" + data.get('href')

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


def get_video_info(html_sources):
    data_list = []
    for html in html_sources:
        soup = BeautifulSoup(html, 'lxml')
        
        script_tags = soup.select('#scriptTag')
        
        if len(script_tags) > 0:
            script_data = json.loads(script_tags[0].text)
            print('script_data ====== : {} '.format(script_data))
            tags = script_data.get('description').split('\n\n')[0]
            view_count = script_data.get('interactionCount')
            published_date = script_data.get('uploadDate')
            title = script_data.get('name')
            
            channel_tag = soup.select('yt-formatted-string#text.ytd-channel-name > a')
            if len(channel_tag) > 0:
                channel_text = channel_tag[0].text

            pd_data = {'title': title, 'channel': channel_text, 'published_date': published_date, 'view_count': view_count, 'tags': tags}    
            print('========= pd_data : {} ======='.format(pd_data))
            # youtube_pd = pd.DataFrame(pd_data, index=[0])
            data_list.append(pd_data)
    
    return data_list

def convert_dataframe(keyword, data_list):
    df = pd.DataFrame(data_list)
    df.to_csv('{}.csv'.format(keyword), sep='|', na_rep='', index=False, encoding='utf-8-sig')
    print('make csv Done')