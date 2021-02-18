from bs4 import BeautifulSoup
import requests
import csv


def movie_mate_info():
    soup = connection()
    connection(soup)


def connection():
    # movie url
    link = 'https://www.imdb.com/list/ls055592025/'
    movie_page = requests.get(link)
    soup = BeautifulSoup(movie_page.content, features="html.parser")
    return soup


def collection(soup):
    soup = connection()
    list_items = soup.findAll("div", {"class": "lister-item"})
    # csv
    file_csv = open('movie_meta_info.csv', 'w+')
    csv_writer = csv.writer(file_csv)
    csv_head = ["index", "title", "year", "certificate", "runtime", "genre", "rate", "metaScore", "brief_description",
                "votes", "gross",
                "description"]
    csv_writer.writerow(csv_head)
    # each item is a movie content
    for item in list_items:
        header = item.find("h3", {"class": "lister-item-header"})
        title = header.find("a").text
        year = header.find("span", {"class": "lister-item-year"}).text
        index = header.find("span", {"class": "lister-item-index"}).text
        certificate = check(item.find("span", {"class": "certificate"}))
        runtime = item.find("span", {"class": "runtime"}).text
        genre = item.find("span", {"class": "genre"}).text
        rate = item.find("span", {"class": "ipl-rating-star__rating"}).text
        meta_score = check(item.find("span", {"class": "metascore"}))
        # brief description
        con = item.find("div", {"class": "lister-item-content"})
        brief_description = check(con.find("p", {"class": ""}))
        # Director
        # Stars
        # votes & gross
        if item.findAll("span", {"name": "nv"}):
            votes = item.findAll("span", {"name": "nv"})[0]['data-value']
            if len(item.findAll("span", {"name": "nv"})) > 1:
                gross = item.findAll("span", {"name": "nv"})[1]['data-value']
            else:
                gross = "NA"
        else:
            votes = "NA"
            gross = "NA"
        # list description TODO each line split
        description = check(item.find("div", {"class": "list-description"}))

        row = [index, title, year, certificate, runtime, genre, rate, meta_score, brief_description, votes, gross,
               description]
        csv_writer.writerow(row)
    csv_writer.close()


def check(obj):
    if obj:
        return obj.text
    else:
        return "NA"


def get_title_names():
    title_name_list = []
    soup = connection()
    list_items = soup.findAll("div", {"class": "lister-item"})
    for item in list_items:
        header = item.find("h3", {"class": "lister-item-header"})
        title = header.find("a").text
        title_name_list.append(title)
    return title_name_list
