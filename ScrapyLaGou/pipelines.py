# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings


class ScrapylagouPipeline(object):

    def __init__(self):
        # 整体内容进行md5后排重
        self.set_model = set()
        self.table = None
        self.db = None
        self.cursor = None

    # 初始化时指定要操作的文件
    def open_spider(self, spider):
        config = {
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }
        # 数据库相关参数从settings文件中读取
        settings = get_project_settings()
        config['host'] = settings.get('HOST')
        config['port'] = settings.get('PORT')
        config['user'] = settings.get('USER')
        config['password'] = settings.get('PASSWORD')
        config['db'] = settings.get('DB')
        self.table = settings.get('TABLE')

        # Connect to the database
        self.db = pymysql.connect(**config)
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # 对所有字段使用md5排重
        md5_content = item.get_md5()
        if md5_content not in self.set_model:
            self.set_model.add(md5_content)
        else:
            # 数据已经存在
            self.logger.debug('数据已经存在,丢弃')
            return item

        try:
            data = item.__dict__['_values']
            keys = ', '.join(data.keys())
            values = ', '.join(['%s'] * len(data))
            sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=self.table, keys=keys, values=values)
            # 执行sql语句
            self.cursor.execute(sql, tuple(data.values()))
            # 提交到数据库执行
            self.db.commit()
        except Exception as e:
            print('发生错误' + str(e))
            # 如果发生错误则回滚
            self.db.rollback()
        # 关闭数据库连接
        return item

    # 处理结束后关闭数据库
    def close_spider(self, spider):
        self.db.close()
