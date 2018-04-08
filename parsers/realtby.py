from argparse import ArgumentParser
import urllib.parse

import requests
from lxml import etree


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('price_min', type=int)
    parser.add_argument('price_max', type=int)
    parser.add_argument('rooms_1', type=int)
    parser.add_argument('rooms_2', type=int)
    parser.add_argument('--with-words', nargs='+', default=[])

    args = parser.parse_args()

    assert args.price_min > 0 and args.price_max > 0 and args.price_min < args.price_max
    assert args.rooms_1 > 0 and args.rooms_2 > 0 and args.rooms_1 <= 8 and args.rooms_2 <= 8

    return args

def get_search(price_min, price_max, rooms_min, rooms_max):
    assert isinstance(price_min, int)
    assert isinstance(price_max, int)
    assert isinstance(rooms_min, int) 
    assert isinstance(rooms_max, int)
    assert price_min > 0 and price_max > 0 and price_min < price_max
    assert rooms_min > 0 and rooms_max > 0 and rooms_min < rooms_max

    params = [
        'eID=tx_uedbcore_mapApi',
        'tid=2001',
        'R=0',
        'type=count',
        'hash=7760dbfc0d863dccd0fba54ee70e0cda', # TODO
        's[state_region_id][e]=',
        's[state_district_id][e]=',
        's[town_id][e]=',
        's[town_name][like][0]=',
        's[town_name][like][1]=',
        's[town_name][like][2]=',
        's[town_name][like][3]=',
        's[town_name][like][4]=',
        's[street_name][like][0]=',
        's[house_number][range][0]=',
        's[street_name][like][1]=',
        's[house_number][range][1]=',
        's[street_name][like][2]=',
        's[house_number][range][2]=',
        's[street_name][like][3]=',
        's[house_number][range][3]=',
        's[street_name][like][4]=',
        's[house_number][range][4]=',
        f's[rooms][e][1]={rooms_min}',
        f's[rooms][e][2]={rooms_max}',
        's[storeys][ge]=',
        's[storeys][le]=',
        's[storey][ge]=',
        's[storey][le]=',
        's[term_of_lease][e]=',
        's[prepayment][e]=',
        's[terms][e]=',
        f's[price][ge]={price_min}',
        f's[price][le]={price_max}',
        's[x_days_old][e]=',
        's[agency_id][e]=',
        'tx_uedbflatrent_pi2[rec_per_page]=30', # max value (10, 20, 30, 50 (not working))
        'tx_uedbflatrent_pi2[sort_by][0]=',
        'tx_uedbflatrent_pi2[asc_desc][0]=0',
        'tx_uedbflatrent_pi2[sort_by][1]=',
        'tx_uedbflatrent_pi2[asc_desc][1]=0',
        's[x_only_private][e]=1',
        's[x_count_pictures][ge]=1',
        'c1=',
        'cat=long'
    ]

    url = f'https://realt.by?' + '&'.join(params)
    resp = requests.get(url)

    count = resp.json()['count']
    search_key = resp.json()['search']

    return count, search_key

def get_search_url(search_key, page=1):
    assert isinstance(search_key, str)
    assert isinstance(page, int)

    return f'https://realt.by/rent/flat-for-long/?search={urllib.parse.quote_plus(search_key)}&page={page}'

def parse_search(search_key):
    assert isinstance(search_key, str)

    resp = requests.get(get_search_url(search_key))

    tree = etree.HTML(resp.text)
    last_page = int(tree.xpath('//*[contains(@class, "uni-paging")][1]/span/span/a/text()')[0])

    aparts = []

    for page in range(1, last_page + 1):
        resp = requests.get(get_search_url(search_key, page))
        tree = etree.HTML(resp.text.split('<!-- INNER-CONTENT -->')[1].split('<!-- menu -->')[0])

        items = tree.xpath('//*[@class = "bd-table"]/*[@class = "bd-table-item "]')

        for item in items:
            _item = item.xpath('.//*[@class = "ad"]/a')[0]
            link = _item.attrib['href']
            address = _item.attrib['title']
            
            descr = item.xpath('.//*[@class = "text"]/p')[0].text

            aparts.append({
                'link': link,
                'address': address,
                'descr': descr if descr else ''
            })

    return aparts


if __name__ == '__main__':
    args = parse_args()

    count, search_key = get_search(args.price_min, args.price_max, args.rooms_1, args.rooms_2)
    print(f'Total filtered flats count: {count}')
    
    aparts = parse_search(search_key)

    true_aparts = []

    for apart in aparts:
        for word in args.with_words:
            if word.lower() in apart['descr'].lower():
                true_aparts.append(apart)

    for apart in true_aparts:
        print(apart['link'])
