import requests
from bs4 import BeautifulSoup
import time
import json
from filters import filters

max_page = 10


def detect_max_page(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find(class_='pages').findChildren('a')
    last_page = pages[-2].text
    print('Last page was detected {}'.format(last_page))
    return int(last_page)


def init():
    i = 1
    page_items = []
    while i <= max_page:
        page_items.append(get_page(i))
        i += 1

        if i <= max_page:
            print('Wait 3 seconds')
            time.sleep(3)
            print('Go to next page \n\n')

    with open('data.json', 'w') as outfile:
        json.dump(page_items, outfile)


def get_page(page_number):
    print('Request to page {}'.format(page_number))
    filters['p'] = page_number
    r = requests.get('https://stopgame.ru/games/filter/', params=filters)
    print('Request to page {} successful'.format(page_number))

    if page_number == 1:
        global max_page
        last_page = detect_max_page(r.text)
        if last_page:
            max_page = last_page

    result = parse_items(r.text)
    return result


def parse_items(text):
    print('Start parsing')
    soup = BeautifulSoup(text, 'html.parser')
    items = soup.find_all(class_='game-summary')
    games = []

    for item in items:
        title = item.find('div', {'class': 'caption'}).findChildren('a')[0].text
        platforms = []
        game_specs = item.findAll('div', {'class': 'game-spec'})[0].findChildren('a')
        for spec in game_specs:
            platforms.append(spec.text)

        games.append({'title': title, 'platforms': platforms})

    print('Parsing successful')
    return games


if __name__ == '__main__':
    init()
