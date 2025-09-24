# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

import redis


# useful for handling different item types with a single interface


class CryptocurrencyprojectPipeline:
    def __init__(self, redis_url):
        self.redis_url = redis_url
        self.redis_client = None

    @classmethod
    def from_crawler(cls, crawler):
        # 从 settings 中获取 REDIS_URL
        redis_url = crawler.settings.get('REDIS_URL')
        return cls(redis_url=redis_url)

    def open_spider(self, spider):
        # 打开 spider 时连接 Redis
        self.redis_client = redis.from_url(self.redis_url)

    def close_spider(self, spider):
        # 关闭 spider 时断开 Redis 连接
        if self.redis_client:
            self.redis_client.connection_pool.disconnect()

    def process_item(self, item, spider):
        data = {
            '名称': item.get("name"),
            '最新价格': item.get("latest_price"),
            '最新涨跌幅': item.get("latest_change_percent"),
            '7天涨跌幅': item.get("seven_days_change_percent"),

            '市场总量': item.get("market_cap"),
            '今日交易货币量': item.get("volume"),
            '今日交易金额': item.get("turnover"),
            '流通量与供应量比值': item.get("circulating_supply_ratio"),
        }

        key = f"{item.get('code')}"
        self.redis_client.set(key, json.dumps(dict(item), ensure_ascii=False))
        return item