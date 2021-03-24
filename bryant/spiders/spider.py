import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import BryantItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class BryantSpider(scrapy.Spider):
	name = 'bryant'
	start_urls = ['https://www.bryantbank.com/resources/blog/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class,"eg-herbert-hoover-element-0")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="byline"]/text()').get().split('on ')[1]
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//section[@class="entry-content"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=BryantItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
