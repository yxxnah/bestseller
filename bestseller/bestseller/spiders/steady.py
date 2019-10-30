import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import urllib.parse
from urllib.parse import urljoin
from urllib.parse import unquote
from bestseller.items import BestsellerItem

# 스테디셀러 수집 클래스
class scrapWeekly(scrapy.Spider):
    name = "bestseller"
    start_urls = [
      'https://ridibooks.com/bestsellers/general?order=steady',
    ]

    def parse(self, response):
        for info in response.css('div.book_macro_110:not(.recommended_book)'):
            detail_page_url = info.css('div.book_thumbnail_wrapper > div.book_thumbnail > a.thumbnail_btn::attr(href)').get()

            item = BestsellerItem()
            item['ranking'] = info.css('p.book_ranking::text').get().strip()
            item['title'] = info.css('div.book_metadata_wrapper > h3 > a > span.title_text::text').get().strip()
            item['author'] = info.css('div.book_metadata_wrapper > p.author > a::text').get().strip()
            item['score'] = info.css('div.book_metadata_wrapper > p.star_rate > span.RSGBookMetadata_StarRate > span.StarRate_Score::text').get()

            # 콜백 요청
            yield scrapy.Request(urllib.parse.unquote(response.urljoin(detail_page_url)), meta={'item':item}, callback=self.parse_detail)

        next_page_url = response.css('li.btn_next > a::attr(href)').get()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_detail(self, response):

        item = response.request.meta['item']
        item['introduce'] = response.css("div#introduce_book > p.introduce_paragraph::text").get().strip(),

        yield item