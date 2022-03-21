import sys
from youtube_crawling import *


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('검색어 입력 필요')
        sys.exit()

    query_string = sys.argv[1]
    titles, urls = get_urls_from_youtube_with_keyword(query_string)
    html_sources = crawl_youtube_page_html_sources(urls)
    data_list = get_video_info(html_sources)
    convert_dataframe(query_string, data_list)