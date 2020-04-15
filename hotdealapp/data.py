from bs4 import BeautifulSoup
import requests

def get_title_fmk(title):
    # return title
    return str(title.text).strip()[:len(title)-6]

def get_fmk(target="title_content", key="만두"):
    '''
    target : 검색범위
        title_content : 제목 + 내용 (default)
        title : 제목
        content : 내용
    key : 검색어
        default = 만두
    '''

    fmk_base_url = "https://www.fmkorea.com"
    base_url = "https://www.fmkorea.com/?vid=&mid=hotdeal&category=&listStyle=webzine&"
    keyword = key
    target = target

    url = base_url + f"search_keyword={keyword}&" + f"search_target={target}"
    request = requests.get(url)
    parsed_data = BeautifulSoup(request.text, "html.parser")

    title_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > h3 > a")
    title_list = map(get_title_fmk, title_list)
    
    link_list = parsed_data.select("h3 > a")
    link_list = map(lambda x:fmk_base_url + f"{x.attrs['href']}", link_list)

    price_list = parsed_data.select("#bd_1196365581_0 > div > div.fm_best_widget._bd_pc > ul > li > div > div.hotdeal_info > span:nth-child(2)")
    price_list = map(lambda x: (x.text)[4:], price_list)
    
    context = {
        "title_list": title_list,
        "link_list": link_list,
        "price_list": price_list,
    }

    return context

get_fmk()