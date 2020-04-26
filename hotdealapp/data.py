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
    
    article_list = list(parsed_data.select('tr.list0, tr.list1'))
    
    today_date = datetime.today()

    result = []
    for article in article_list:
        date = article.select_one("nobr.eng").text
        try:
            article_date = today_date - datetime.strptime(date, "%y/%m/%d")
        except ValueError:
            article_date = today_date - today_date

        if article_date >= timedelta(days=days_delta):
            continue

        end = article.select_one("span.list_comment2 + img")
        if end == None:
            try:
                date = datetime.strptime(date, "%y/%m/%d").strftime("%Y-%m-%d")
            except ValueError:
                date = date[:5]

            title_with_link = article.select_one("td[valign='middle'] > a")
            title = title_with_link.select_one("font").text
            link = ppmp_base_url + title_with_link.attrs['href']

            img = "http:" + article.select_one("img").attrs['src']
            
            result.append({
                "title": title,
                "link" : link,
                "img": img,
                "date": date,
                "from": "ppmp",
            })
    
    return result



def get_ruliweb(key="만두"):
    
    base_url = "https://bbs.ruliweb.com/ps/board/1020?search_type=subject&search_key="
    keyword = key

    url = base_url + keyword
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")
    table = parsed_data.select_one("div.board_main.theme_default.theme_white")
    num_notice = len(table.select("tr.inside"))

    articles = parsed_data.select("div.board_main.theme_default.theme_white > table > tbody > tr")[num_notice:]
    today_date = datetime.today()

    result = []
    for article in articles:
        date = article.select_one("td.time").text.strip()
        try:
            article_date = today_date - datetime.strptime(date, "%Y.%m.%d")
        except ValueError:
            article_date = today_date - today_date
        
        if article_date >= timedelta(days=days_delta):
            break

        title_with_link = article.select_one("td.subject a")
        title = title_with_link.text.strip()
        if "품절" in title or "종료" in title:
            break
        link = title_with_link.attrs['href']
        img = None

        try:
            date = datetime.strptime(date, "%Y.%m.%d").strftime("%Y-%m-%d")
        except ValueError:
            pass
            
        result.append({
            "title": title,
            "link": link,
            "img": img,
            "date": date,
            "from": "ruliweb",
        })

    return result
