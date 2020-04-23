from pprint import pprint

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import time

# from . import apikey


fmk_base_url = "https://www.fmkorea.com/"
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

def get_fmk(key="만두"):
    
    today_date = datetime.today()

    base_url = "https://www.fmkorea.com/?vid=&mid=hotdeal&category=&listStyle=webzine&"
    keyword = key

    # html parsing
    url = "{}search_keyword={}&search_target=title".format(base_url, keyword)
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")
    
    article_list = parsed_data.select("div.fm_best_widget li")

    result = []
    for article in article_list:
        date = article.select("span.regdate")[0].text.strip()
        try:
            date = datetime.strptime(date, "%Y.%m.%d").strftime("%Y-%m-%d")
        except ValueError:
            pass

        try:
            article_date = today_date - datetime.strptime(date, "%Y.%m.%d")
        except ValueError:
            article_date = today_date - today_date

        if article_date >= timedelta(days=days_delta):
            continue

        title = article.select("h3")[0].text.strip()
        index = title.rfind("[")
        title = title[:index-1]
        
        link = article.select("a:nth-child(2)")[0].attrs["href"]
        link = fmk_base_url + link.split("srl=")[1].split("&")[0]
        
        try:
            img = "https:" + article.select("img.thumb")[0].attrs["data-original"]
        except IndexError:
            img = None
        result.append({
            "title": title,
            "link": link,
            "date": date,
            "img": img,
            "from": 'fmk',
        })

    return result

def get_ppmp(key="만두"):

    base_url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page_num=20&category="
    keyword = key

    url = base_url + "&search_type=subject" + f"&keyword={keyword}"
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    # date_list 만들기
    date_list = parsed_data.select("nobr.eng")
    date_list = list(map(lambda x: x.text, date_list))

    # title_list 저장, 만료여부 테스트
    valid_title_idx = []
    title_list = list(parsed_data.select("td[valign='middle'] > a > font"))
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




def get_ruliweb(key="만두"):
    
    base_url = "https://bbs.ruliweb.com/ps/board/1020?search_type=subject&search_key="
    keyword = key

    url = base_url + keyword
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    # date_list
    n = len(parsed_data.select("tr.notice"))
    b = len(parsed_data.select("tr.best"))
    date_list = parsed_data.select("td.time")[n+b:]
    date_list = list(map(lambda x: x.text.strip(), date_list))
    
    # title_list, link_list, validation
    title_link_list = parsed_data.select("td.subject > div.relative > a.deco")
    title_list = []
    link_list = []
    for data in title_link_list:
        title_list.append(data.text)
        link_list.append(data.attrs["href"])
    
    valid_title_idx = []
    today_date = datetime.today()

    for idx, data in enumerate(title_list):
        if "품절" not in data and "종료" not in data:
            try:
                article_date = today_date - datetime.strptime(date_list[idx], "%Y.%m.%d")
            except ValueError:
                article_date = today_date - today_date
            
            if article_date < timedelta(days=days_delta):
                valid_title_idx.append(idx)

    result = []
    for i in valid_title_idx:
        try:
            date = datetime.strptime(date_list[i], "%Y.%m.%d").strftime("%Y-%m-%d")
        except ValueError:
            date = date_list[i]
        result.append({
            "title": title_list[i],
            "link": link_list[i],
            "date": date
        })

    return result
