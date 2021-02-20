import json
from urllib.parse import urlparse
import certifi
import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver


# get screenplay from www.simplayscripts.com
# input: titles : movie's titles, it's a list titles=['','']
# output: semi-structured screenplays information to a json file

def get_screenplays_from_simply_scripts(titles):
    url = 'https://www.simplyscripts.com/movie-screenplays.html'
    browser = webdriver.Firefox()
    browser.get(url)
    movie_content = browser.find_element_by_id("movie_wide")
    screenplay_url_list = []
    has_no_script_titles = []
    for title in titles:
        links = movie_content.find_elements_by_partial_link_text(title)
        if not links:
            has_no_script_titles.append(links)
        else:
            for link in links:
                screenply_map = {}
                screenply_map.update({"title": title})
                screenplay_url = link.get_attribute("href")
                screenply_map.update({"screenplay_url": screenplay_url})
                screenplay_url_list.append(screenply_map)
                parent_p = link.find_element_by_xpath("..")
                text = parent_p.find_element_by_tag_name("span").text
                screenply_map.update({"text": text})
    # has_no_script_titles = list(dict.fromkeys(has_no_script_titles))
    # print(has_no_script_titles)
    with open('scripts_simply.json', 'w+') as outfile:
        json.dump(screenplay_url_list, outfile)
    return 'scripts_simply.json'


def batch_download(filename):
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for item in data:
            title = item['title']
            url = item['screenplay_url']
            download(title, url)
    return True


def download(title, url):
    url_obj = urlparse(url)
    path = url_obj.path.lower()
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    resp = http.request('GET', url)
    suffix = ""
    if path.endswith(".txt"):
        suffix = ".txt"
    elif path.endswith(".html"):
        suffix = ".html"
    elif path.endswith(".pdf"):
        suffix = ".pdf"
    file = open("screenplays/"+title + suffix, 'wb')
    file.write(resp.data)
    file.close()


# get screenplay from www.dailyscripts.com
# input: titles : movie's titles, it's a list titles=['','']
# output: semi-structured screenplays information to a json file

def get_screenplays_from_daily_scripts(titles):
    url_a_m = "https://www.dailyscript.com/movie.html"
    url_n_z = "https://www.dailyscript.com/movie_n-z.html"
    movie_page_a = requests.get(url_a_m)
    movie_page_b = requests.get(url_n_z)
    soup_a = BeautifulSoup(movie_page_a.content, features="html.parser")
    soup_b = BeautifulSoup(movie_page_b.content, features="html.parser")
    items_a = soup_a.findAll("p")
    items_b = soup_b.findAll("p")
    script_list = []
    for title in titles:
        has_script = False
        for item in items_a:
            script = parse_script(title, item)
            if script:
                script_list.append(script)
                has_script = True
        for item in items_b:
            script = parse_script(title, item)
            if script:
                script_list.append(script)
                has_script = True
        # if not has_script:
        #     print(title)
    with open('scripts_daily.json', 'w+') as outfile:
        json.dump(script_list, outfile)
    return 'scripts_daily.json'


def parse_script(title, item):
    domain = "https://www.dailyscript.com/"
    script = {}
    # a
    movie_a = item.find("a", string=title)
    if movie_a and movie_a.text == title:
        script_url = domain + movie_a.get("href")
        script.update({"screenplay_url": script_url})
        # text
        # movie_des = item.text
        script.update({"title": title})
        # script.update({"desc": movie_des})
        # imdb
        movie_imdb = item.find("a", string="imdb")
        if movie_imdb:
            script.update({"imdb": movie_imdb.get("href")})
        return script
    else:
        return ""
