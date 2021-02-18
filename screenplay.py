import csv
import json
import string
from urllib.parse import urlparse
import certifi
import requests
import urllib3
from bs4 import BeautifulSoup
from selenium import webdriver

from movie_mate_info import get_title_names


def screenplay():
    screenplay_url_list = get_screenplay_url_list()
    for key, value in screenplay_url_list[0].items():
        print(key, value)
        download(key, value)


def get_screenplay_url_list():
    titles = get_title_names()
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
            index = 0
            for link in links:
                screenplay_url = link.get_attribute("href")
                if check_url_path(screenplay_url):
                    screenply_map = {title + "_" + str(index): screenplay_url}
                    screenplay_url_list.append(screenply_map)
                    index = index + 1
    has_no_script_titles = list(dict.fromkeys(has_no_script_titles))
    print(has_no_script_titles)
    return screenplay_url_list


def save_ref():
    screenplay_list = get_screenplay_url_list()
    file = open('screenplay.csv', 'w+')
    writer = csv.writer(file)
    for script in screenplay_list:
        for title, url in script.items():
            row = [title, url]
            writer.writerow(row)
    file.close()


def check_url_path(url):
    url_obj = urlparse(url)
    path = url_obj.path.lower()
    if path.endswith(".html") or path.endswith(".txt") or path.endswith(".pdf"):
        return True
    else:
        return False


def download(title, url):
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    resp = http.request('GET', url)
    file_ = open(title + ".txt", 'wb')
    file_.write(resp.data)
    file_.close()


def search():
    titles = get_title_names()
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
            script = get_script(title, item)
            if script:
                script_list.append(script)
                has_script = True
        for item in items_b:
            script = get_script(title, item)
            if script:
                script_list.append(script)
                has_script = True
        if not has_script:
            print(title)
    with open('script.json', 'w+') as outfile:
        json.dump(script_list, outfile)
    return script_list


def get_script(title, item):
    domain = "https://www.dailyscript.com/"
    script = {}
    # a
    movie_a = item.find("a", string=title)
    if movie_a and movie_a.text==title:
        script_url = domain + movie_a.get("href")
        if check_url_path(script_url):
            script.update({"link": script_url})
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
