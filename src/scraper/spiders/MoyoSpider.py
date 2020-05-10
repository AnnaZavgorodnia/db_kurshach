import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.spiders import Spider, Request


class MoyoSpider(Spider):
    name = 'moyo'
    start_urls = [
        'https://www.moyo.ua/comp-and-periphery/notebooks/?perPage=96?page=1']
    last_page_num = None

    def parse(self, response):
        items = Selector(response=response) \
            .xpath('//div[@class="product-tile_inner_wrapper"]')

        for item in items:
            yield self.parse_item(item, response.url)

        if not self.last_page_num:
            last_nav_el = Selector(response).xpath('//a[@class="new-pagination-link"][last()]/text()').get()
            self.last_page_num = int(last_nav_el)

        next_page_url, next_page_num = increase_page_number(response.url)
        if next_page_num <= self.last_page_num:
            yield Request(next_page_url,
                          callback=self.parse)

    @staticmethod
    def parse_item(item, main_url):
        specs = item.xpath('.//div[@class="specifications_content"]')

        return {
            'name': item.xpath('.//div[@class="product-tile_title ddd"]//text()').get().replace('Ноутбук', '').strip(),
            'cpu_frequency': parse_cpu_freq(specs.xpath('./div[5]/text()').get()),
            'ram': parse_ram(specs.xpath('./div[6]/text()').get()),
            'memory': parse_memory(specs.xpath('./div[10]/text()').get()),
            'weight': parse_weight(specs.xpath('./div[last()]/text()').get()),
            'price': parse_price(item.xpath('.//span[@class="product-tile_price-value"]/text()').get()),
            'origin_url': urljoin(main_url, item.xpath('.//a[@class="gtm-link-product"]/@href').get())
        }


def parse_cpu_freq(freq):
    try:
        min_, max_ = freq.split('-')
        return float(max_.replace(',', '.'))
    except ValueError:
        return float(remove_non_numeric(freq).replace(',', '.'))


def parse_ram(ram):
    return int(remove_non_numeric(ram))


def parse_memory(memory):
    if not memory or not remove_non_numeric(memory):
        return 256
    if ',' in memory:
        hdd, ssd = memory.split(',')[:2]
        return parse_memory(hdd) + parse_memory(ssd)
    if '+' in memory:
        return parse_memory(memory.replace('+', ','))
    if 'ТБ' in memory:
        return int(remove_non_numeric(memory)) * 1024
    return int(remove_non_numeric(memory))


def parse_weight(weight):
    try:
        return float(weight.replace(',', '.'))
    except ValueError:
        return 2.5


def parse_price(price):
    return int(remove_non_numeric(price))


def remove_non_numeric(line):
    return re.sub('[^0-9,]', '', line)


def increase_page_number(url):
    base, page = url.split('page=')
    new_page_number = int(page) + 1
    return f'{base}page={new_page_number}', new_page_number
