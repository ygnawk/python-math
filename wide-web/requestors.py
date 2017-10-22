"""
To spam views on blogs

to begin make sure that you are connected tor, then do

    url = "https://mail.google.com"
    structured_sr(url,100,100)

"""

import web
import tor
import threading


def persistent_request(url: str) -> None:
    "request until successful"
    try:
        web.request(url, random=True)
    except:
        persistent_request(url)


def successive_request(url: str, n: int) -> None:
    "requests data from the url n times at once"
    req = lambda: persistent_request(url)
    for i in range(n):
        threading.Thread(target=req).start()
        print(
            "<--Request Number %s Sent from Thread %s -->                 \033[A"
            % (i, threading.get_ident()))


def structured_sr(url: str, n: int, t: int) -> None:
    "requests data continuously but with delay depending on connection speed"

    def req() -> None:
        for i in range(n):
            print(
                "<--Request Number %s Sent from Thread %s -->            \033[A"
                % (i, threading.get_ident()))
            persistent_request(url)
    for i in range(t):
        threading.Thread(target=req).start()
