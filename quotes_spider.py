# 1. scrapy 모듈을 가져옵니다
import scrapy

# 2. scrapy.crawler로부터 CrawlerProcess 클래스를 가져옵니다
# 2-1. CrawlerProcess 클래스는 크롤링을 실행하고 관리하는데 사용됩니다
from scrapy.crawler import CrawlerProcess

# 3. scrapy.Spider 클래스를 상속받는 새로운 클래스(QuotesSpider)를 정의합니다
class QuotesSpider(scrapy.Spider):
    
    # 4. 이름을 정의, 이름은 스파이더를 실행할 때 사용됩니다
    name = "quotes"
    
    # 5. 스파이더가 크롤링하는 URL리스트를 정의합니다
    start_urls = ['http://quotes.toscrape.com/page/1/']

    # 6. parse 메서드를 정의합니다
    # 6-1. 메서드는 URL에서 응답을 받았을 때 호출됩니다
    def parse(self, response):
        
        # 7. CSS 선택자를 사용하여 모든 div 태그 중에 클래스가 quote인 요소를 반복합니다
        for quote in response.css('div.quote'):
            
            # 8. 각 인용문에서 텍스트와 저자를 추출하여 딕셔너리 형태로 반환합니다
            # 8-1. yield는 이 데이터를 Scrapy의 데이터 파이프라인으로 전달합니다
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('span.small::text').get(),
            }

        # 9. 다음 페이지로 가는 링크의 href 속성을 추출합니다
        next_page = response.css('li.next a::attr(href)').get()
        
        # 10. 만약 다음 페이지가 존재한다면, response.follow 메서드를 사용하여 다음 페이지를 크롤링합니다
        # 10-1. 이때 parse 메서드를 다시 호출해서 재귀적으로 크롤링을 진행합니다
        if next_page is not None:
            yield response.follow(next_page, self.parse)

# Scrapy 프로세스를 시작하는 코드
# 11. 
process = CrawlerProcess(settings={
    'FEEDS': {
        'quotes.csv': {
            'format': 'csv',
            'encoding': 'utf8',
            'store_empty': False,
            'fields': ['text', 'author'],
            'indent': 4,
        },
    },
})
process.crawl(QuotesSpider)
process.start()
