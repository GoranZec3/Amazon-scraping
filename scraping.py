import csv
from bs4 import BeautifulSoup
import requests


def get_url(search_term):
    '''Generate a url from search term'''
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search_term = search_term.replace(' ', '+')

    #add term query to url
    url = template.format(search_term)

    #add page query placeholder
    url += '&page={}'

    return url

def extract_records(item):
    '''Extract and return data from a single record'''
    #description and url
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href') #get url

    try:
        #price
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        #rank and rating
        rating = item.i.text
        review_count = item.find('span', {'class':'a-size-base s-underline-text'}).text
    #skip empty fields
    except AttributeError:
        rating = ''
        review_count = ''

    results = (description, price, rating, review_count, url)

    return results


def main(search_term, number_of_pages):
    '''Run main program routine'''
    # HEADER
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
              'Accept-Language': 'en-US, en;q=0.5'}

    records = []
    pages = range(1,number_of_pages) #number of pages

    #iterate through pages
    for page in pages:
        url = get_url(search_term).format(page)
        webpage = requests.get(url, headers=header)
        soup = BeautifulSoup(webpage.content, 'lxml')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        #iterate through page for items
        for item in results:
            record = extract_records(item)
            if record:
                records.append(record)

    #save data
    with open('results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'ReviewCount', 'Url'])
        writer.writerows(records)


try:
    main('rtx 3060', 4) #search term, number of pages to iterate

except KeyboardInterrupt:
    pass
