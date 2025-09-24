# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CryptocurrencyprojectItem(scrapy.Item):
    name = scrapy.Field()  # 名称
    code = scrapy.Field()  # 代码
    latest_price = scrapy.Field()  # 最新价
    latest_change_percent = scrapy.Field()  # 最新涨跌幅
    seven_days_change_percent = scrapy.Field()  # 7天涨跌幅

    market_cap = scrapy.Field()  # 市场总量
    volume = scrapy.Field()  # 交易量
    turnover = scrapy.Field()  # 交易额
    circulating_supply = scrapy.Field()  # 流通供应量
