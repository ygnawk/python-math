"""
A url parser really
"""

import http.client
import header


class RedirectedException(Exception):
    "An exception showing that the page was redirected"

    def __init__(self, description: str, value: str) -> None:
        self.link = value
        self.description = description

    def __str__(self) -> str:
        return repr(self.description)


class parse_http:
    "parse url string"
    __slots__ = "mode", "host", "subdomain", "security", "url"

    def format_url(self, url: str) -> tuple:
        security, link = url.split("//")
        host, *subdomain = link.split('/')
        subdomain = '/' + "/".join(subdomain)
        return security, host, subdomain

    def __init__(self, url: str) -> None:
        self.url = url
        if not url.lower().startswith("http"):
            raise http.client.HTTPException("not a valid HTTP link")

        security, host, subdomain = self.format_url(url)

        if security.lower().startswith("http:"):
            self.mode = http.client.HTTPConnection
        elif security.lower().startswith("https:"):
            self.mode = http.client.HTTPSConnection
        else:
            raise http.client.InvalidURL("parse error %s" % url)

        self.security = security + "//"
        self.host = host
        self.subdomain = subdomain


def connection_success(string_url: str) -> bool:
    "check if the requests successfully connects"
    url = parse_http(string_url)
    client = url.mode(url.host)
    client.request("GET", "/", headers=header.static_header())
    response = client.getresponse()

    if response.status // 100 == 4 or response.status // 100 == 5:
        raise http.client.HTTPException("HTTP error %s: %s" % (
            response.status, response.reason), response)

    elif response.status // 100 == 3:
        link = response.headers['Location']
        if not link.lower().startswith("http"):
            link = url.security + url.host + link
        raise RedirectedException("redirected to %s" % link, link)

    elif response.status % 100 == 2:
        return True
    return False


def follow_redirect(string_url: str) -> str:
    "follows redirects and returns the direct url"
    try:
        connection_success(string_url)
    except RedirectedException as link:
        string_url = follow_redirect(link.link)
    return string_url


def get_response(string_url: str) -> http.client.HTTPResponse:
    "get response from a url"
    url = parse_http(string_url)
    client = url.mode(url.host)
    client.request("GET", "/", headers=header.false_header())
    return client.getresponse()


"""

client = http.client.HTTPConnection('hugelol.com')
client.request("GET","/lol/395756", headers = header.false_header())
response = client.getresponse()
html = response.read()
header = response.headers
print(response.__dict__)
print(response.status,response.reason)
print(str(html,'utf-8'))


"""
