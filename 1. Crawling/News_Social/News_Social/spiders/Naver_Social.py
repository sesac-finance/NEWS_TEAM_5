import scrapy
import datetime


class NaverSocialSpider(scrapy.Spider):
    name = 'Naver_Social'
    allowed_domains = ['news.naver.com']
    start_urls = ['http://news.naver.com/']


    def start_requests(self):
        for term in range(0, 30):
        # datetime을 이용한 특정 기간 출력 (20221101 ~ 20221130)
            date = (datetime.date(2022, 11, 1) + datetime.timedelta(+term)).strftime('%Y%m%d')
            pages = range(1, 350)
            subcategory_lists = ['249', '250', '251', '252', '254', '255', '256', '257', '276', '59b']

            for i in range(len(subcategory_lists)):
                sub = subcategory_lists[i]

                # 네이버 뉴스 주소 형태 : https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=249&sid1=102&date=20221130&page=2
                # 249 -> 서브카테고리 고유번호
                # 249 - 사건사고, 250 - 교육, 251 - 노동, 252 - 환경, 254 - 언론, 255 - 식품/의료, 256 - 지역, 257 - 사회 일반, 276 - 인물, 59b - 인권/복지-
                # 102 -> 메인카테고리 고유번호(사회)
                # date= -> 날짜
                # page= -> 페이지

                for page in pages:
                    urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={0}&sid1=102&date={1}&page={2}'.format(sub, date, page)
                    headers = {"user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

                    yield scrapy.Request(url=urls, headers = headers, callback=self.parse_link)


    def parse_link(self, response):
        
        # 서브카테고리 목록
        subcategory = response.xpath('//*[@id="main_content"]/div[1]/h3/text()').extract()

        # href
        news_selects = response.css('.type06_headline > li')
        for news_select in news_selects:
            for href in news_select.css('dl dt > a[href]::attr(href)'):
                url = response.urljoin(href.extract())
                
                yield scrapy.Request(url, callback=self.parse_dir_contents, meta={'subcategory':subcategory})


    def parse_dir_contents(self, response):

        item={}

        # 기사 본문
        full_text = response.css('#dic_area::text').extract()
        content = []
        for text in full_text:
            content.append(text.strip())

        maincategory = response.xpath('//*[@id="_LNB"]/ul/li[4]/a/span/text()').extract()
        subcategory = response.meta.get('subcategory')

        date = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/@data-date-time').extract()
        title = response.xpath('//*[@id="title_area"]/span/text()').extract()

        url = response.xpath('/html/head/meta[6]').get().split('content=')[1].split('>')[0]
        photourl = response.xpath('//*[@id="img1"]').get().split('src=')[1].split(' ')[0]

        writer = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[2]/a/em/text()').extract()
        press = response.xpath('//*[@id="ct"]/div[1]/div[1]/a/img[1]/@alt').extract()

        item['MainCategory'] = maincategory
        item['SubCategory'] = subcategory
        item['WritedAt'] = date
        item['Title'] = title
        item['Content'] = content
        item['URL'] = url
        item['PhotoURL'] = photourl
        item['Writer'] = writer
        item['Press'] = press


        print(item)
        return item