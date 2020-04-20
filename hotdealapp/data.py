from pprint import pprint

from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import requests
import time

# from . import apikey


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

def get_fmk(key="만두"):
    
    base_url = "https://www.fmkorea.com/?vid=&mid=hotdeal&category=&listStyle=webzine&"
    keyword = key

    # html parsing
    url = "{}search_keyword={}&search_target=title".format(base_url, keyword)
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


def weather():
    weather_url = f'https://api.openweathermap.org/data/2.5/onecall?lat=36.11&lon=128.34&appid=dc6fd7a40851c1bddcb20eea52f18325&lang=kr'
    response = requests.get(weather_url).json()
    current = response.get('current')
    # 현재 온도
    current_temp = current.get('temp') - 273.15
    # 현재 날씨 ex) "Clear" "Clounds" "Rain" "Snow"
    current_weather = current.get('weather')[0].get('icon')
    current_clouds = current.get('clouds')
    current_time = time.strftime("%H:%M:%S", time.gmtime(current.get('dt') + 32400))

    # 시간별
    hourly = response.get('hourly')
    hourly_datas = []
    for i in range(1, 25, 3):
        # 기온, 날씨, 구름양, 시간
        hourly_datas += [hourly[i].get('temp') - 273.15, hourly[i].get('weather')[0].get('icon'), hourly[i].get('clouds'), time.strftime("%H:%M:%S", time.gmtime(hourly[i].get('dt') + 32400))]
    result = [0]
    for i in range(0, len(hourly_datas), 4):
        result.append({
            "temp": round(hourly_datas[i], 1),
            "weather": hourly_datas[i+1],
            "clouds": hourly_datas[i+2],
            "time": hourly_datas[i+3][:5],
        })
    # 하루
    daily = response.get('daily')
    # 하루의 최저기온, 최고기온z
    daily_data = [daily[0].get('temp').get('min') - 273.15, daily[0].get('temp').get('max') - 273.15]
    dict_weather = {
        'current_temp': round(current_temp, 1),
        'current_weather': current_weather,
        'current_clouds': current_clouds,
        'current_time': current_time,
        'daily_min': round(daily[0].get('temp').get('min') - 273.15, 1),
        'daily_max': round(daily[0].get('temp').get('max') - 273.15, 1),
        'hourly_datas': result
    }

    return dict_weather