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
# 11. CrawlerProcess 클래스의 인스턴스를 생성하고 설정을 지정합니다
process = CrawlerProcess(settings={
    
    # 12. FEEDS 설정은 
    'FEEDS': {
        # 12-1. 데이터를 quotes.csv에 저장하도록 합니다
        'quotes.csv': {
            # 12-2. 형식은 csv로
            'format': 'csv',
            # 12-3. 인코딩은 UTF-8로
            'encoding': 'utf8',
            # 12-4. 빈 항목은 저장하지 않고
            'store_empty': False,
            # 12-5. 저장할 필드는 text와 author로
            'fields': ['text', 'author'],
            # 12-6. 들여쓰기는 4칸으로 설정합니다
            'indent': 4,
        },
    },
})

# 13. process 인스턴스에 QuotesSpider 스파이더를 등록합니다
process.crawl(QuotesSpider)

# 14. 크롤링을 시작합니다
# 14-1. 크롤리이 시작된 후 스크립트의 실행을 차단하고 크롤링이 완료될 때까지 대기합니다
process.start()
