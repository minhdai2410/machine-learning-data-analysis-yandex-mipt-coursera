import requests
import bs4
from multiprocessing import Pool
from functools import reduce

def getAllTags(url, tag, attrs):
    req = requests.get(url)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    return parser.findAll(tag, attrs)
    
def parse_page(url):
    divs = getAllTags(url, 'div', 'recenses-item__content')
    return [div.get_text(separator="\n") + '\n' for div in divs]
    
if __name__ == '__main__':    
    main_url = 'https://www.litres.ru/knigi-fentezi/'
    req = requests.get(main_url)
    parser = bs4.BeautifulSoup(req.text, 'lxml')
    book_tags = parser.findAll('a', attrs={'class':'img-a'})
    books_urls = ['https://pda.litres.ru' + str(book_tag['href']) + 'otzivi/' for book_tag in book_tags]

    p = Pool(8)
    map_results = p.map(parse_page, books_urls)
    reduce_results = reduce(lambda x,y: x + y, map_results)
    
    with open('parsing_results.txt','w', encoding="utf-8") as file:
        file.write('\n'.join(reduce_results))
