# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from repository.repo import RepositoryProduct

class CrawlerPipeline:
    def process_item(self, item, spider):
            
        item: ItemAdapter = ItemAdapter(item)
        if item.get('price'):
            item['price'] = int(item['price'].replace('.', ''))
        
        if item.get('decimal'):
            item['decimal'] = int(item['decimal'])/100
            item['price'] += item['decimal']
        
        item.pop('decimal')
        RepositoryProduct().insert_product(item.asdict())
        return item
