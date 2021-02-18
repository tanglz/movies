import csv
from urllib.parse import urlparse

# Press the green button in the gutter to run the script.
from screenplay import save_ref, download, search, get_screenplay_url_list

if __name__ == '__main__':
    # collection()
    # find_url("test")
    # screenplay()
    # link="https://www.dailyscript.com/scripts/Godfather,%20The.txt"
    # link="https://web.archive.org/web/20160221233643/http://www.pages.drexel.edu/~ina22/splaylib/Screenplay-Godfather,%20The-Continuity.pdf"
    link = "https://www.dailyscript.com/scripts/Godfather,%20The.txt"
    title = "Goodfellas_0"
    # download(title, link)
    # The Godfather_0
    # save_ref()
    # file = open('Goodfellas_0.txt', 'r')
    # lines = file.readlines()
    # index = 0
    # for line in lines:
    #     if line.strip():
    #         print(str(index)+":" + line.strip())
    #         index = index + 1
    #         if "INT" in line.strip():
    #             break
    # search()
    get_screenplay_url_list()