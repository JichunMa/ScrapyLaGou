# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.utils.project import get_project_settings

from ScrapyLaGou.items import ScrapylagouItem
from urllib.parse import urlencode, quote_plus


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def parse(self, response):
        json_dict = json.loads(response.text)
        if json_dict['success'] is True:
            content = json_dict['content']
            position_result = content['positionResult']
            result = position_result['result']
            for item in result:
                if item['stationname'] is None:
                    item['stationname'] = '未知'
                info = ScrapylagouItem()

                info['title'] = item['positionName']
                info['address'] = item['stationname']
                info['salary'] = item['salary']
                info['workYear'] = item['workYear']
                info['company'] = item['companyFullName']
                info['financeStage'] = item['financeStage']
                yield info

    def start_requests(self):

        base_url = 'https://www.lagou.com/jobs/positionAjax.json?'
        base_args = {'city': '北京', 'needAddtionalResult': False}
        final_url = base_url + urlencode(base_args, quote_via=quote_plus)
        settings = get_project_settings()
        pages = settings.get('PAGES')

        request_args = {'first': 'true', 'pn': '1', 'kd': '安卓'}
        for page in range(1, pages):
            request_args['pn'] = str(page)
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=final_url,
                formdata=request_args,
                callback=self.parse)
