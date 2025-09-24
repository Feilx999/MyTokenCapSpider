import hashlib
import json
import logging
import time
from urllib.parse import urlencode

import scrapy
from fake_useragent import UserAgent


class MytokencapspiderSpider(scrapy.Spider):
    name = "MyTokenCapSpider"
    url = 'https://api.mytoken.info/ticker/currencyranklist'


    @staticmethod
    def get_head():
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'no-cache',
            'origin': 'https://www.mytokencap.com',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://www.mytokencap.com/',
            'sec-ch-ua': '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': UserAgent(browsers=['chrome', 'firefox', 'edge'],
                                    os=['windows']
                                    ).random
        }

        return headers

    @staticmethod
    def get_code():
        t = str(int(time.time() * 1000))
        s = t + '9527' + t[:6]
        code = hashlib.md5(s.encode('utf-8')).hexdigest()
        return {
            'code': code,
            'timestamp': int(t)
        }

    def get_params(self, page):
        code_dict = self.get_code()
        params = {
            'pages': f'{page},1',
            'sizes': '100,100',
            'subject': 'market_cap',
            'language': 'en_US',
            'legal_currency': 'USD',
            'code': code_dict['code'],
            'timestamp': code_dict['timestamp'],
            'platform': 'web_pc',
            'v': '0.1.0',
            'mytoken': '',
        }
        return params

    async def start(self):
        for i in range(1, 2):   # 只取一页做测试
            url = self.url + "?" + urlencode(self.get_params(i))
            yield scrapy.Request(
                url=url,
                headers=self.get_head(),
                callback=self.parse,
                dont_filter= True,
            )

    def parse(self, response):
        if response.status == 200:
            logging.warning(f"请求成功:{response.url}")
        else:
            logging.warning(f"请求失败,状态码 {response.status}:{response.url}")
        data = json.loads(response.text)["data"]['list']
        num = 0
        for item in data:
            num += 1
            mytokencap_item = {
                'name': item.get("symbol"),
                'code': item.get("id", f"{num:05d}"),
                'latest_price': item.get("global_price_second_price_display"),
                'latest_change_percent': f"{item.get("percent_change_24h")}%",
                'seven_days_change_percent': f"{item.get("percent_change_7d")}%",

                'market_cap': item.get("market_cap_display"),
                'volume': f"{item.get("volume_24h_from")} 个",
                'turnover': f"$ {item.get("volume_24h_usd")}",
                'circulating_supply': f"{item.get("circulating_supply")}%",
            }
            yield mytokencap_item

