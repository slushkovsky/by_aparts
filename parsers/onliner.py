import urllib.parse
from argparse import ArgumentParser
from typing import Iterable, List

import requests
from lxml import etree

from db import SearchResult


def parse_args():
    parser = ArgumentParser()

    parser.add_argument('price_min', type=int)
    parser.add_argument('price_max', type=int)
    parser.add_argument('rooms', nargs='+')
    parser.add_argument('--with-opts', nargs='+', default=[])
    parser.add_argument('--without-opts', nargs='+', default=[])
    parser.add_argument('--with-words', nargs='+', default=[])
    parser.add_argument('--previous-results', action='store_true', help='Show all results including which was found earlier')

    args = parser.parse_args()

    args.rooms = [int(n) for n in args.rooms]

    return args


def make_url(price_min: int, price_max: int, rooms: Iterable[int], page: int, only_owner: bool = True) -> str:
    assert price_min > 0 and price_max > 0 and price_min < price_max
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

    query_part = urllib.parse.urlencode(params) + ''.join([f'&rent_type[]={n}_room{"s" if n > 1 else ""}' for n in rooms])

    return f'https://ak.api.onliner.by/search/apartments?{query_part}'


def parse_aparts(price_min: int, price_max : int, rooms: Iterable[int], only_owner: bool = True) -> List[dict]:
    assert price_min > 0 and price_max > 0 and price_max > price_min

    url = make_url(price_min, price_max, rooms, page=1, only_owner=only_owner)
    resp = requests.get(url)

    max_page = resp.json()['page']['last']

    results: List[dict] = []

    for i, page in enumerate(range(1, max_page + 1)):
        url = make_url(price_min, price_max, rooms, page=page, only_owner=only_owner)
        resp = requests.get(url)

        results += resp.json()['apartments']

        print(f'Parse aparts list: page {i}/{max_page} ...', end='\r')

    print(f'Parse aparts lits: DONE ({max_page} pages, {len(results)} aparts)')

    return results


def apart_option(tree, name: str) -> bool:
    found = tree.xpath(f'//*[contains(@class, "apartment-options__item")][text() = "{name}"]')
    assert len(found) == 1
    found = found[0]

    return 'apartment-options__item_lack' not in found.attrib['class']


def apart_descr(tree) -> str:
    descr_elem = tree.xpath('//*[contains(@class, "apartment-info__line")]//*[contains(@class, "apartment-info__cell_66")]//*[contains(@class, "apartment-info__sub-line_extended-bottom")]')

    if len(descr_elem) == 0:
        return ''

    assert len(descr_elem) == 1

    descr_elem = descr_elem[0]

    return ''.join(list(descr_elem.itertext()))


def check_apart_opts(url: str, with_opts: Iterable[str], without_opts: Iterable[str], with_words: Iterable[str]) -> bool:
    assert url.startswith('http')

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

    descr = apart_descr(tree)

    for word in with_words:
        if not word.lower() in descr.lower():
            return False

    return True


if __name__ == '__main__':
    args = parse_args()

    aparts = parse_aparts(args.price_min, args.price_max, args.rooms)
    true_aparts: List[dict] = []

    for i, apart in enumerate(aparts):
        print(f'Parse apart pages: {i}/{len(aparts)} ... (found: {len(true_aparts)})', end='\r')

        if check_apart_opts(apart['url'], args.with_opts, args.without_opts, args.with_words):
            true_aparts.append(apart)

    print(f'Parse apart pages: DONE ({len(aparts)})' + ' '*20)

    true_aparts_urls = [apart['url'] for apart in true_aparts]

    printed = 0
    skiped = 0

    for url in true_aparts_urls:
        is_known_result = SearchResult.select().where(SearchResult.url == url).exists()

        if not is_known_result or (is_known_result and args.previous_results):
            print(url)
            printed += 1
        else:
            skiped += 1

        if not is_known_result:
            SearchResult.create(url=url)

    print(f'Count: {printed} printed + {skiped} hidden (was found earlier, use --previous-results to display)')
