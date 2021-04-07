import scrapy

from scrapy.loader import ItemLoader

from ..items import WaynesavingsItem
from itemloaders.processors import TakeFirst


class WaynesavingsSpider(scrapy.Spider):
	name = 'waynesavings'
	start_urls = ['https://www.waynesavings.com/RESOURCES/OUR-BANK/News']

	def parse(self, response):
		post_links = response.xpath('//div[@class="edn_readMoreButtonWrapper"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="article_pager"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="edn_articleTitle"]/text()').get()
		description = response.xpath('(//article//p | //article//ul)//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get().split('on')[1]

		item = ItemLoader(item=WaynesavingsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
