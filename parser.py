import urllib.parse
from pprint import pprint
from argparse import ArgumentParser

import requests
from lxml import etree


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('price_min', type=int)
    parser.add_argument('price_max', type=int)
    parser.add_argument('rooms', nargs='+')
    parser.add_argument('--with-opts', nargs='+', default=[])
    parser.add_argument('--without-opts', nargs='+', default=[])

    args = parser.parse_args()

    args.rooms = [int(n) for n in args.rooms]

    return args

def make_url(price_min, price_max, rooms, page, only_owner=True):
    assert isinstance(price_min, int)
    assert isinstance(price_max, int)
    assert price_min > 0 and price_max > 0 and price_min < price_max
    assert isinstance(rooms, list)
    assert all((isinstance(room, int) for room in rooms))
    assert isinstance(only_owner, bool)
    assert isinstance(page, int)
    assert page > 0

    params = {
        'price[min]': price_min,
        'price[max]': price_max,
        'currency': 'usd',
        'only_owner': 'true' if only_owner else 'false',
        'bounds[lb][lat]': 53.760473464187534,
        'bounds[lb][long]': 27.263404244164413,
        'bounds[rt][lat]': 54.042088515398746,
        'bounds[rt][long]': 27.76189333742789, 
        'page': page
    }

    return 'https://ak.api.onliner.by/search/apartments?' + urllib.parse.urlencode(params) + ''.join([f'&rent_type[]={n}_room{"s" if n > 1 else ""}' for n in rooms])

def parse_aparts(price_min, price_max, rooms, only_owner=True):
    assert isinstance(price_min, int)
    assert isinstance(price_max, int)
    assert price_min > 0
    assert price_max > 0
    assert price_max > price_min
    assert isinstance(rooms, list)
    assert all((isinstance(n, int) for n in rooms))
    assert isinstance(only_owner, bool)

    url = make_url(price_min, price_max, rooms, page=1, only_owner=only_owner)
    resp = requests.get(url)

    max_page = resp.json()['page']['last']

    results = []

    for i, page in enumerate(range(1, max_page + 1)):
        url = make_url(price_min, price_max, rooms, page=page, only_owner=only_owner)
        resp = requests.get(url)

        results += resp.json()['apartments']

        print(f'Parse aparts list: page {i}/{max_page} ...', end='\r')

    print(f'Parse aparts lits: DONE ({max_page} pages, {len(results)} aparts)')

    return results

def apart_option(tree, name):
    assert isinstance(name, str)

    found = tree.xpath(f'//*[contains(@class, "apartment-options__item")][text() = "{name}"]')
    assert len(found) == 1
    found = found[0]

    return not 'apartment-options__item_lack' in found.attrib['class']


def check_apart_opts(url, with_opts, without_opts):
    assert isinstance(url, str)
    assert url.startswith('http')
    assert isinstance(with_opts, list)
    assert isinstance(without_opts, list)
    assert all((isinstance(opt, str) for opt in with_opts))
    assert all((isinstance(opt, str) for opt in without_opts))

    resp = requests.get(url)
    tree = etree.HTML(resp.text)
   
    for opt in with_opts:
        value = apart_option(tree, opt)
        assert isinstance(value, bool)
        if not value:
            return False

    for opt in without_opts:
        value = apart_option(tree, opt)
        assert isinstance(value, bool)
        if value:
            return False

    return True


if __name__ == '__main__':
    args = parse_args()

    aparts = parse_aparts(args.price_min, args.price_max, args.rooms)
    true_aparts = []

    for i, apart in enumerate(aparts):
        print(f'Parse apart pages: {i}/{len(aparts)} ... (found: {len(true_aparts)})', end='\r')

        if check_apart_opts(apart['url'], args.with_opts, args.without_opts):
            true_aparts.append(apart)

    print(f'Parse apart pages: DONE ({len(aparts)})')

    for apart in true_aparts:
        print(apart['url'])
