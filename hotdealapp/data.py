from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests

fmk_base_url = "https://www.fmkorea.com"
ppmp_base_url = "http://www.ppomppu.co.kr/zboard/"

days_delta = 5

def get_title_fmk(title):
    title = str(title.text)
    for i in range(len(title)-1, -1, -1):
        if title[i] == "[":
            idx = i
            break
    return title[:i].strip()

def get_article_id_fmk(data):
    url = data.attrs["href"]
    result = url.split("document_srl=")
    result = result[1].split("&")[0]
    return fmk_base_url + "/" + result

def get_article_id_ppmp(data):
    url = data.attrs["href"]
    return ppmp_base_url + url

def get_fmk(target=2, key="만두"):
    '''
    target : 검색범위
        1 = title : 제목
        2 = title_content : 제목 + 내용 (default)
    key : 검색어
        default = 만두
    '''
    
    base_url = "https://www.fmkorea.com/?vid=&mid=hotdeal&category=&listStyle=webzine&"
    keyword = key
    if target == 1:
        target = "title"
    else:
        target = "title_content"

    # html parsing
    url = "{}search_keyword={}&search_target={}".format(base_url, keyword, target)
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    # date_list 만들기
    date_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > div:last-child > span.regdate")
    date_list = list(map(lambda x: x.text.strip(), date_list))

    # title_list 만들고 날짜, 만료여부 저장
    valid_title_idx = []
    title_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > h3 > a")
    
    today_date = datetime.today()
    
    for index, title in enumerate(title_list):
        if title.attrs["class"][0] == "hotdeal_var8":
            try:
                article_date = today_date - datetime.strptime(date_list[index], "%Y.%m.%d")
                
            except ValueError:
                article_date = today_date - today_date

            if article_date < timedelta(days=days_delta):
                valid_title_idx.append(index)
    title_list = list(map(get_title_fmk, title_list))
    
    # link_list 만들기
    link_list = parsed_data.select("h3 > a")
    link_list = list(map(get_article_id_fmk, link_list))

    # price_list 만들기
    price_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > div.hotdeal_info > span:nth-child(2) > a")
    price_list = list(map(lambda x: (x.text), price_list))
    
    result = []
    for i in valid_title_idx:
        try:
            date = datetime.strptime(date_list[i], "%Y.%m.%d").strftime("%Y-%m-%d")
        except ValueError:
            date = date_list[i]
        result.append({
            "title": title_list[i],
            "price": price_list[i],
            "link": link_list[i],
            "date": date,
        })

    return result

def get_ppmp(target=2, key="만두"):
    '''
    target : 검색범위
        1 = subject : 제목
        2 = sub_memo : 제목 + 내용 (default)
    key : 검색어
        default = 만두
    '''

    base_url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page_num=20&category="
    keyword = key
    if target == 1:
        target = "subject"
    else:
        target = "sub_memo"
    
    # html parsing
    url = base_url + f"&search_type={target}" + f"&keyword={keyword}"
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    # date_list 만들기
    date_list = parsed_data.select("nobr.eng")
    date_list = list(map(lambda x: x.text, date_list))

    # title_list 저장, 만료여부 테스트
    valid_title_idx = []
    title_list = list(parsed_data.select("font.list_title"))
    title_list = list(map(lambda x: x.text ,title_list))

    today_date = datetime.today()

    title_data = list(parsed_data.select("td[valign='middle']"))
    for idx, data in enumerate(title_data):
        is_expired = data.select_one("span.list_comment2 + img")
        if not is_expired:
            try:
                article_date = today_date - datetime.strptime(date_list[idx], "%y/%m/%d")
            except ValueError:
                article_date = today_date - today_date
            
            if article_date < timedelta(days=days_delta):
                valid_title_idx.append(idx)

    # link_list 저장
    link_list = parsed_data.select("td[valign='middle'] > a")
    link_list = list(map(get_article_id_ppmp, link_list))

    result = []
    for i in valid_title_idx:
        try:
            date = datetime.strptime(date_list[i], "%y/%m/%d").strftime("%Y-%m-%d")
        except ValueError:
            date = date_list[i][:5]
        result.append({
            "title": title_list[i],
            "link": link_list[i],
            "date": date,
        })
    
    return result

