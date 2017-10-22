"""
Tor Module

Import this module to connect to Tor

dependency: tor on macport
            socksipy

to start, initialize tor on terminal
make sure that global variable HOST and PORT
matches the default settings of macport

run script normally

to connect to tor, type:
connect Tor
"""

import socket
import urllib.request
import urllib.error
import bs4
import socks

HOST = "127.0.0.1"
PORT = 9050
BROWSER_VERSION = 'Mozilla/5.0 (Window`s NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
CONNECTED_MESAGE = '\n    \n      Congratulations. This browser is configured to use Tor.\n    \n'
HEADER = {
    'User-Agent': BROWSER_VERSION,
    'Referer': 'http://www.google.com/'
}


def connect_tor():
    "Connect to Tor"
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, HOST, PORT, True)
    socket.socket = socks.socksocket


def request(url: str):
    "Returns request object of the url"
    req = urllib.request.Request(url, headers=HEADER)
    return urllib.request.urlopen(req)


def get_html(url: str, encoding: str='utf-8') -> str:
    "returns html string of the url"
    html = request(url).read()
    html = str(html, encoding)
    b_soup = bs4.BeautifulSoup(html, 'html.parser')
    return str(b_soup.prettify())


def soup(url: str, encoding: str='utf-8') -> bs4.BeautifulSoup:
    "returns beautiful soup html parser of the url"
    html = request(url).read()
    html = str(html, encoding)
    b_soup = bs4.BeautifulSoup(html, 'html.parser')
    return b_soup


def connected(printing) -> bool:
    "check if connected to Tor"
    tor_noodle = soup("https://check.torproject.org/")
    title = str(tor_noodle.title.string)

    length = len("<strong>")
    ip_tor = tor_noodle.find_all("strong")[0]
    ip_heroku = get_html("http://my-ip.herokuapp.com/").split("\n")[1][9:-1]
    ip_icanhazip = get_html("http://icanhazip.com/")[:-1]

    if printing:
        print("Your IP appears to be", ip_heroku, "at Heroku")
        print("Your IP appears to be", str(ip_tor)[length:-length - 1],
              "at the Tor webpage")
        print("Your IP appears to be", ip_icanhazip, "at icanhazip.com")
        print(title)
    if title == CONNECTED_MESAGE:
        return True
    return False


def connect(printing = True) -> None:
    "initialize the script"
    connect_tor()
    if not connected(printing = printing):
        raise ConnectionError("not connected to Tor")


connect()
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
print(s.getsockname())
s.close()


