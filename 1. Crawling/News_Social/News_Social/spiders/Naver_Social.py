import scrapy
import datetime
import pandas as pd
# from News_Social.items import NewsSocialItem

class NaverSocialSpider(scrapy.Spider):
    name = 'Naver_Social'
    allowed_domains = ['news.naver.com']
    start_urls = ['http://news.naver.com/']

    # def start_requests(self):
    #     for term in range(0, 30): # 30으로 바꾸기
    #     # datetime을 이용한 특정 기간 출력 (20221101 ~ 20221130)
    #         date = (datetime.date(2022, 11, 1) + datetime.timedelta(+term)).strftime('%Y%m%d')
    #         pages = range(1, 350) # 사회일반때문에 350 (확인 결과 최대 316p)
    #         subcategory_lists = ['249', '250', '251', '252', '254', '255', '256', '257', '276', '59b']

    #         for i in range(len(subcategory_lists)):
    #             sub = subcategory_lists[i]
    #             for page in pages:
    #                 urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={0}&sid1=102&date={1}&page={2}'.format(sub, date, page)
    #                 headers = {"user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

    #                 yield scrapy.Request(url=urls, headers = headers, callback=self.parse_link)


    def start_requests(self):
        for term in range(0, 1): # 30으로 바꾸기
        # datetime을 이용한 특정 기간 출력 (20221101 ~ 20221130)
            date = (datetime.date(2022, 11, 17) + datetime.timedelta(+term)).strftime('%Y%m%d')
            pages = range(300, 317) # 사회일반때문에 300..
            subcategory_lists = ['257']

            for i in range(len(subcategory_lists)):
                sub = subcategory_lists[i]
                for page in pages:
                    urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={0}&sid1=102&date={1}&page={2}'.format(sub, date, page)
                    headers = {"user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

                    yield scrapy.Request(url=urls, headers = headers, callback=self.parse_link)


    def parse_link(self, response):
        subcategory = response.xpath('//*[@id="main_content"]/div[1]/h3/text()').extract()
        news_sels = response.css('.type06_headline > li')
        for news_sel in news_sels:
            for href in news_sel.css('dl dt > a[href]::attr(href)'):
                url = response.urljoin(href.extract())
                yield scrapy.Request(url, callback=self.parse_dir_contents, meta={'subcategory':subcategory})


    def parse_dir_contents(self, response):

        item={}

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
        press = response.xpath('//*[@id="ct"]/div[1]/div[1]/a/img[1]/@alt').extract()

        #stickers_useful = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[1]/a/span[1]/text()').extract()
        #stickers_useful_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[1]/a/span[2]/text()').extract()
    
        #stickers_wow = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[2]/a/span[1]/text()').extract()
        #stickers_wow_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[2]/a/span[2]/text()').extract()
    
        #stickers_touched = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[3]/a/span[1]/text()').extract()
        #stickers_touched_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[3]/a/span[2]/text()').extract()
    
        #stickers_analytical = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[4]/a/span[1]/text()').extract()
        #stickers_analytical_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[4]/a/span[2]/text()').extract()
    
        #stickers_recommend = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[5]/a/span[1]/text()').extract()
        #stickers_recommend_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[5]/a/span[2]/text()').extract()

        item['MainCategory'] = maincategory
        item['SubCategory'] = subcategory
        item['WritedAt'] = date
        item['Title'] = title
        item['Content'] = content
        item['URL'] = url
        item['PhotoURL'] = photourl
        item['Press'] = press
        #item['Stickers'] = stickers_useful+stickers_useful_count, stickers_wow+stickers_wow_count, stickers_touched+stickers_touched_count, stickers_analytical+stickers_analytical_count, stickers_recommend+stickers_recommend_count


        print(item)
        return item




###############################




    # def start_requests(self):
        
    #     # subcate_lists ={'사건사고':'249', '교육':'250', '노동':'251', '언론':'254', '환경':'252', '인권/복지':'59b', '식품/의료':'255', '지역':'256',  '인물':'276',  '사회_일반':'257'}
    #     # # for sub_name, sub_num in subcate_lists.items():
    #     # subcategory = []
    #     # for i in subcate_lists.keys():
    #     #     subcategory.append(i)         

        

    #     for term in range(0, 2): # 30으로 바꾸기
    #         # datetime을 이용한 특정 기간 출력 (20221101 ~ 20221130)
    #         date = (datetime.date(2022, 11, 1) + datetime.timedelta(+term)).strftime('%Y%m%d')

    #         pages = range(1,2)

    #         subcategory_lists = ['249', '250', '251', '252', '254', '255', '256', '257', '276', '59b']
    #         # for sub_li in subcategory:
    #         for i in range(len(subcategory_lists)):
    #             sub = subcategory_lists[i]
    #         # urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2=249&sid1=102&date=20221130&page=2'
    #             for page in pages:
    #                 urls = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid2={0}&sid1=102&date={1}&page={2}'.format(sub, date, page) #.format(sub_list) #, date3, page)
    #                 headers = {"user-agent" : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
                

    #                 yield scrapy.Request(url=urls, headers = headers, callback=self.parse_link) #, meta=subcate_lists) # meta = sub~~~




    # def parse_link(self, response):

    #     subcategory = response.xpath('//*[@id="main_content"]/div[1]/h3/text()').extract()

    #     news_links = response.css('.type06_headline > li')
    #     for news_link in news_links:
    #         for href in news_link.css('dl dt > a[href]::attr(href)'):
    #             url = response.urljoin(href.extract())
    #             yield scrapy.Request(url, callback=self.parse_dir_contents, meta={'subcategory':subcategory}) #, meta=subcate_lists #, meta = subcategory


    # def parse_dir_contents(self, response):

    #     item={}

    #     full_text = response.css('#dic_area::text').extract() # newsct_article _article_body
    #     content = []
    #     for text in full_text:
    #         content.append(text.strip())
        
    #     # maincategory = response.css('.media_end_categorize_item::text').extract()[0]

    #     maincategory = response.xpath('//*[@id="_LNB"]/ul/li[4]/a/span/text()').extract()

    #     subcategory = response.meta.get('subcategory')

    #     # dates = response.css('.media_end_head_info_datestamp_time::text').get().split(' ') #[1] @data-date-time
    #     date = response.xpath('//*[@id="ct"]/div[1]/div[3]/div[1]/div/span/@data-date-time').extract()

    #     title = response.xpath('//*[@id="title_area"]/span/text()').extract()

    #     url = response.xpath('/html/head/meta[6]').get().split('content=')[1].split('>')[0]
    #     photourl = response.xpath('//*[@id="img1"]').get().split('src=')[1].split(' ')[0]
    #     press = response.xpath('//*[@id="ct"]/div[1]/div[1]/a/img[1]/@alt').extract()

    #     # stickers_dict = {}
        
    #     # stickers_useful = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[1]/a/span[1]/text()').extract()
    #     # stickers_useful_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[1]/a/span[2]/text()').extract()
        
    #     # stickers_wow = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[2]/a/span[1]/text()').extract()
    #     # stickers_wow_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[2]/a/span[2]/text()').extract()
        
    #     # stickers_touched = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[3]/a/span[1]/text()').extract()
    #     # stickers_touched_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[3]/a/span[2]/text()').extract()
        
    #     # stickers_analytical = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[4]/a/span[1]/text()').extract()
    #     # stickers_analytical_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[4]/a/span[2]/text()').extract()
        
    #     # stickers_recommend = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[5]/a/span[1]/text()').extract()
    #     # stickers_recommend_count = response.xpath('//*[@id="likeItCountViewDiv"]/ul/li[5]/a/span[2]/text()').extract()

    #     # stickers_dict = {stickers_useful:stickers_useful_count, stickers_wow:stickers_wow_count, stickers_touched:stickers_touched_count, stickers_analytical:stickers_analytical_count, stickers_recommend:stickers_recommend_count}









    #     item['MainCategory'] = maincategory
    #     item['SubCategory'] = subcategory
    #     item['WritedAt'] = date
    #     item['Title'] = title
    #     item['Content'] = content
    #     item['URL'] = url
    #     item['PhotoURL'] = photourl
    #     item['Press'] = press
    #     # item['Stickers'] = stickers_useful+stickers_useful_count, stickers_wow+stickers_wow_count, stickers_touched+stickers_touched_count, stickers_analytical+stickers_analytical_count, stickers_recommend+stickers_recommend_count
    #     # item['Stickers'] = stickers_dict

    #     print(item)
    #     return item