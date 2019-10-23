import scrapy
import urllib.parse
from urllib.parse import urljoin
from urllib.parse import unquote

# 주간 베스트셀러 수집 클래스
class scrapWeekly(scrapy.Spider):
  name = "bestseller"
  start_urls = [
    'https://ridibooks.com/bestsellers/general',
  ]

  def parse(self, response):
    for item in response.css('div.book_macro_110'):
      yield {
        'ranking': item.css('p.book_ranking::text').get().strip(),
        'title': item.css('div.book_metadata_wrapper > h3 > a > span.title_text::text').get().strip(),
        'author': item.css('div.book_metadata_wrapper > p.author > a::text').get().strip(),
        'score': item.css('div.book_metadata_wrapper > p.star_rate > span.RSGBookMetadata_StarRate > span.StarRate_Score::text').get().strip()
      }

    next_page_url = response.css('li.page_this + li > a::attr(href)').extract_first()
    if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))