import re
from urllib.parse import urljoin

from scrapy import Selector
from scrapy.spiders import Spider, Request


class FoxtrotSpider(Spider):
    name = 'foxtrot'
    start_urls = ['https://www.foxtrot.com.ua/ru/shop/noutbuki.html']

    def parse(self, response):
        root = Selector(response)

        links = root \
            .xpath('//a[@title]/@href').getall()
        for link in links:
            yield Request(urljoin(response.url, link), callback=self.parse_laptop_page)

        next_page_url = root.xpath('//li[@class="listing__pagination-nav"][last()]/a/@href').get()
        yield Request(urljoin(response.url, next_page_url), callback=self.parse)

    @staticmethod
    def parse_laptop_page(response):
        root = Selector(response)
        content = root.xpath('//div[@class="popup__content"]')
        name = content.xpath('//span[@title]/@title').get()
        cpu_frequency = content.xpath('.//*[contains(text(), "частота процессора")]/../../td[2]/a/text()').get()
        ram = content.xpath('.//*[contains(text(), "ОЗУ")]/../../td[2]/a/text()').get()
        hdd_mem = content.xpath('.//p[contains(text(), "HDD")]/../../td[2]/a/text()').get()
        ssd_mem = content.xpath('.//p[contains(text(), "SSD")]/../../td[2]/a/text()').get()
        weight = content.xpath('.//*[contains(text(), "Вес")]/../../td[2]/a/text()').get()
        price = root.xpath('//div[@class="card-price"]/text()').get()

        return {
            'name': parse_name(name),
            'cpu_frequency': parse_cpu_freq(cpu_frequency),
            'ram': parse_ram(ram),
            'memory': parse_memory(hdd_mem) + parse_memory(ssd_mem),
            'weight': parse_weight(weight),
            'price': parse_price(price)
        }


def parse_name(name):
    return name.replace('Ноутбук', '').replace('игровой', '').strip()


def parse_cpu_freq(freq):
    return float(remove_non_numeric(freq))


def parse_ram(ram):
    return int(remove_non_numeric(ram))


def parse_memory(memory):
    if not memory:
        return 0
    coef = 1024 if 'Тб' in memory else 1
    return int(remove_non_numeric(memory)) * coef


def parse_weight(weight):
    return float(remove_non_numeric(weight))


def parse_price(price):
    return int(remove_non_numeric(price))


def remove_non_numeric(line):
    return re.sub('[^0-9.]', '', line)