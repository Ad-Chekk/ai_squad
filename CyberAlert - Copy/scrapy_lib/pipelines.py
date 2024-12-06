# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyLibPipeline:
    def process_item(self, item, spider):
        return item



import csv
import os

class CsvExportPipeline:
    def open_spider(self, spider):
        os.makedirs('data', exist_ok=True)  # Create a 'data' directory if it doesn't exist
        self.file = open('data/scrapy_data.csv', 'w', newline='')  # Save the CSV in the 'data' directory
        self.writer = csv.writer(self.file)
        self.writer.writerow(['URL', 'Status Code', 'Response Time (s)', 'Depth', 'Data Extracted'])

def close_spider(self, spider):
        stats = spider.crawler.stats.get_value('custom_data', [])
        for stat in stats:
            self.writer.writerow([
                stat.get('url', ''),
                stat.get('status_code', ''),
                stat.get('response_time', ''),
                stat.get('depth', ''),
                stat.get('data_extracted', '')
            ])
        self.file.close()

def process_item(self, item, spider):
    for stat in spider.crawler.stats.get_value('custom_data', []):
        if stat['url'] == item.get('url'):
            stat['data_extracted'] = dict(item)
    return item
