"""
Web Library


"""

import header
import urllib.request
import urllib.error
import bs4
import random
import http.client
#import tor


def request(url: str, random: bool=False):
    "returns the request object of the url"
    head = header.random_header() if random else header.static_header()
    req = urllib.request.Request(url, headers=head)
    return urllib.request.urlopen(req)


def get_html(url: str) -> str:
    "returns the html string of the url"
    return request(url).read()


def download(url: str, path: str) -> None:
    "Go to the link and retrive the designated content. Save it at the path"
    f = open(path, 'wb')
    data = request(url, path)
    f.write(data)
    f.close()


def get_soup(url: str, encoding: str='utf-8', parser = 'html.parser'):
    "return a BeautifulSoup parser of the html at the  url"
    html = request(url).read()
    html = str(html, encoding)
    soup = bs4.BeautifulSoup(html, parser)
    return soup
