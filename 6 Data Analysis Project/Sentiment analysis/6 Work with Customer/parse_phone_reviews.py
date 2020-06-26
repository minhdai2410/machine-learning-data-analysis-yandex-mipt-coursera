import requests
import bs4
from multiprocessing import Pool
from functools import reduce
import pandas as pd
import numpy as np

def getAllTags(url, tag, attrs):
    req = requests.get(url)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    return parser.findAll(tag, attrs)
    
def parse_urls(url):
    url_tags = getAllTags(url, 'a', 'model-short-title')
    urls = ['https://www.e-katalog.ru/review' + tag['href'][:-4] for tag in url_tags]
    return urls

def div_to_text(div):
    if div is None:
        return None
    else:
        return div.get_text(separator="\n") + '\n'

def parse_review(parser):
    description = div_to_text(parser.find('span', attrs={'itemprop':'description'}))
    title = div_to_text(parser.find('div', 'review-title'))
    plus = div_to_text(parser.find('div', 'review-plus'))
    minus = div_to_text(parser.find('div', 'review-minus'))
    result = ''
    if description is None:
        result = title + plus + minus
    else:
        result = title + description + plus + minus
    return result

def parse_sentiment(parser):
    tag = parser.find('div', 'review-title')
    if tag.find('img')['src'] in ['/img/svg/review-smile-3.svg','/img/svg/review-smile-4.svg']:
        return 1
    else:
        return 0

def parse_sentiment_reviews(url):
    tags = getAllTags(url, 'td', 'review-td')
    reviews_n_classes = []
    for tag in tags:
        review = parse_review(tag)
        class_ = parse_sentiment(tag)
        reviews_n_classes.append([review, class_])
    return reviews_n_classes

def map_n_reduce(function, array, processes=8):
    p = Pool(processes)
    map_ = p.map(function, array)
    return reduce(lambda x,y: x+y, map_)    

if __name__ == '__main__':    
    main_urls = ['https://www.e-katalog.ru/list/122/'] + ['https://www.e-katalog.ru/list/122/' + str(i) for i in np.arange(1,76 + 1)]
    reduce_urls = map_n_reduce(parse_urls, main_urls)
    reviews = map_n_reduce(parse_sentiment_reviews, reduce_urls)
    pd.DataFrame(reviews, columns=['text','class']).to_csv('data/train.csv', index=False)
