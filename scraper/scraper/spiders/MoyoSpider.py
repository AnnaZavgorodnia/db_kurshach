import re

from scrapy import Selector
from scrapy.spiders import Spider, Request


class MoyoSpider(Spider):
    name = 'moyo'
    start_urls = [
        'https://www.moyo.ua/comp-and-periphery/notebooks/?perPage=96?page=1']

    def parse(self, response):
        items = Selector(response=response) \
            .xpath('//div[@class="product-tile_inner_wrapper"]')
        if not items:
            return

        for item in items:
            yield self.parse_item(item)
        yield Request(increase_page_number(response.url),
                      callback=self.parse)

    @staticmethod
    def parse_item(item):
        specs = item.xpath('.//div[@class="specifications_content"]')

        return {
            'name': item.xpath('.//div[@class="product-tile_title ddd"]//text()').get().replace('Ноутбук', '').strip(),
            'cpu_frequency': parse_cpu_freq(specs.xpath('./div[5]/text()').get()),
            'ram': parse_ram(specs.xpath('./div[6]/text()').get()),
            'memory': parse_memory(specs.xpath('./div[10]/text()').get()),
            'weight': parse_weight(specs.xpath('./div[last()]/text()').get()),
            'price': parse_price(item.xpath('.//span[@class="product-tile_price-value"]/text()').get())}


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
    return f'{base}page={int(page) + 1}'
