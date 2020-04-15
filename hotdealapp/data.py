from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

fmk_base_url = "https://www.fmkorea.com"


def get_title_fmk(title):
    # return title
    return str(title.text).strip()[:len(title)-6]

def get_article_id_fmk(url):
    url = url.attrs["href"]
    result = url.split("document_srl=")
    result = result[1].split("&")[0]
    return fmk_base_url + "/" + result

def get_fmk(target="title_content", key="만두"):
    '''
    target : 검색범위
        title_content : 제목 + 내용 (default)
        title : 제목
        content : 내용
    key : 검색어
        default = 만두
    '''

    days_delta = 20
    
    base_url = "https://www.fmkorea.com/?vid=&mid=hotdeal&category=&listStyle=webzine&"
    keyword = key
    target = target

    # html parsing
    url = "{}search_keyword={}&search_target={}".format(base_url, keyword, target)
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    # date_list 만들기
    date_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > div:nth-child(5) > span.regdate")
    date_list = list(map(lambda x: x.text.strip(), date_list))

    # title_list 만들고 날짜, 만료여부 저장
    valid_title_idx = []
    title_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > h3 > a")
    
    today_date = datetime.today()
    print(
        today_date - datetime.strptime(date_list[0], "%Y.%m.%d"),
        timedelta(days=5)
    )
    for index, title in enumerate(title_list):
        if title.attrs["class"][0] == "hotdeal_var8" and (today_date - datetime.strptime(date_list[index], "%Y.%m.%d")) < timedelta(days=days_delta):
            valid_title_idx.append(index)
    title_list = list(map(get_title_fmk, title_list))
    
    # link_list 만들기
    link_list = parsed_data.select("h3 > a")
    link_list = list(map(get_article_id_fmk, link_list))

    # price_list 만들기
    price_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > div.hotdeal_info > span:nth-child(2)")
    price_list = list(map(lambda x: (x.text)[4:], price_list))
    

    result = []
    for i in valid_title_idx:
        result.append({
            "title": title_list[i],
            "price": price_list[i],
            "link": link_list[i],
            "date": datetime.strptime(date_list[i], "%Y.%m.%d").strftime("%Y-%m-%d"),
        })

    return result
