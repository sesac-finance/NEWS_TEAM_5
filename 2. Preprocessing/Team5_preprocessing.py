import sys
import csv
import re


# 2022 새싹 5팀에서 네이버 뉴스(사회, 생활/문화) 크롤링 csv 포맷은,
# 뉴스 본문 article : MainCategory,SubCategory,WritedAt,Title,Content,URL,PhotoURL,Writer,Press,Stickers
# 뉴스 댓글 comments : URL,UserID,UserName,WritedAt,Content
# 위에서 본문 댓글 모두 Content 컬럼 위치는 df[4] 로 동일함.

maxInt = sys.maxsize


while True:
    try:
        # 용량이 큰 뉴스기사를 파싱할 때 에러 방지를 위해서 시스템이 허용하는 최대값을 넣어준다.
        csv.field_size_limit(maxInt)

        with open(r"D:\git\team5\article.csv", 'rt', encoding='UTF-8', newline='') as csvfile:
        
            csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            with open(r"D:\git\team5\Team5_article.csv", 'w', newline='', encoding='UTF8') as f:
                # create a csv writer
                writer = csv.writer(f)

                csv_text = ""
                list_string = []
                new_string = ""

                for i, row in enumerate(csvreader):

                    # 아래에서 row[4] 가 Content 컬럼(본문) 임. 댓글도 동일하게 Content 가 row[4]
                    list_string = re.findall(r"""[ㄱ-ㅣ가-힣]|[ |\,|\.]""",  row[4])
                    
                    # 제목을 원본 CSV와 동일하게 넣어주기 위해서 첫 줄은 처리없이 그대로 써준다.
                    if i == 0 :
                        writer.writerow(row)

                    else :
                        t = ''
                        # 아래에서 본문 기사 하나 즉, csv 파일 Content 컬럼에서 한 줄을 조립하여 만든다(t).
                        # 추가로 띄어쓰기도 함께 하는데 re 정규표현식이 글자단위로 결과를 output 하기 때문임.
                        for x in list_string:
                            if x =='' :
                                t += ' '
                            else :
                                t += x

                        t = t.strip()
                        new_string = re.sub(r"""[\,|\.]""", " ", t)
                        new_string = re.sub(r"""[ ]{2,}""", " ", new_string)
                        new_string = re.sub(r"""[ ]([ㄱ-ㅣ가-힣][ ]).[ ]""", " ", new_string)
                        new_string = re.sub(r"""[ ][ㄱ-ㅣ가-힣][ ]""", " ",new_string)
                        new_string = re.sub(r"""[ ][ㄱ-ㅣ가-힣][ ]""", " ", new_string)
                        new_string = re.sub("\n", "", new_string)
                        

                        row[4] = new_string
                        writer.writerow(row)
        break

    except OverflowError:
        # python3에서 간혹 허용 최대값 적용시 에러가 발생하는데 이를 방지하기 위한 부분 
        maxInt = int(maxInt/10)
            

      
    
        