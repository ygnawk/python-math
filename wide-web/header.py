"""
for request headers for HTTP
"""

from fake_useragent import UserAgent
import random

UA = UserAgent()

ACCEPT_LANG = [
    'en-US', 'en', 'af', 'sq', 'am', 'ar', 'hy',
    'az', 'eu', 'be', 'bn', 'bs', 'br', 'bg', 'ca',
    'zh', 'zh-CN', 'zh-TW', 'co', 'hr', 'cs', 'da',
    'nl', 'en-AU', 'en-CA', 'en-NZ', 'en-ZA', 'en-GB',
    'eo', 'et', 'fo', 'fil', 'fi', 'fr', 'fr-CA',
    'fr-FR', 'fr-CH', 'gl', 'ka', 'de', 'de-AT',
    'de-DE', 'de-LI', 'de-CH', 'el', 'gn', 'gu',
    'ha', 'haw', 'he', 'hi', 'hu', 'is', 'id', 'ia',
    'ga', 'it', 'it-IT', 'it-CH', 'ja', 'kn', 'kk',
    'km', 'ko', 'ku', 'ckb', 'ky', 'lo', 'la', 'lv',
    'ln', 'lt', 'mk', 'ms', 'ml', 'mt', 'mr', 'mn',
    'ne', 'no', 'nb', 'nn', 'oc', 'or', 'om', 'ps',
    'fa', 'pl', 'pt', 'pt-BR', 'pt-PT', 'pa', 'qu',
    'ro', 'mo', 'rm', 'ru', 'gd', 'sr', 'sh', 'sn',
    'sd', 'si', 'sk', 'sl', 'so', 'st', 'es', 'es-419',
    'su', 'sw', 'sv', 'tg', 'ta', 'tt', 'te', 'th', 'ti',
    'to', 'tr', 'tk', 'tw', 'uk', 'ur', 'ug', 'uz', 'vi',
    'cy', 'fy', 'xh', 'yi', 'yo', 'zu']


REFERERS = [
    'https://facebook.com/',
    'https://www.tumblr.com/',

    'https://www.google.co.uk/',
    'https://www.google.co.th/',
    'https://www.google.com.mx/',
    'https://www.google.fr/',
    'https://www.google.ca/',
    'https://www.google.com.vn/',

    'https://www.twitter.com',
    'https://www.pinterest.com/',
    'https://www.instagram.com/',
    'http://www.nytimes.com/'
]

ACCEPT_ENCODING = ['identity', 'gzip', 'deflate', 'sdch']

CONNECTIONS = ['keep-alive', 'close']


def random_header() -> dict:
    "returns a random header"
    header = {
        'User-Agent': UA.random,
        'DNT': '1'
    }

    if random.randrange(4):
        header['Referer'] = random.choice(REFERERS)

    if random.randrange(4):
        multiplicity = random.randrange(1, 4)
        subset = random.sample(ACCEPT_LANG, multiplicity)
        header['Accept-Language'] = ",".join(subset)

    if random.randrange(4):
        multiplicity = random.randrange(1, 4)
        subset = random.sample(ACCEPT_ENCODING, multiplicity)
        header['Accept-Encoding'] = ",".join(subset)

    if random.randrange(3):
        header['Upgrade-Insecure-Requests'] = '1'

    if random.randrange(2):
        header['Cache-Control'] = 'max-age=%s' % (30 * random.randrange(5))
    elif random.randrange(2):
        header['Cache-Control'] = 'no-cache'
    elif random.randrange(2):
        header['Cache-Control'] = 'Expire'

    return header


def false_header() -> dict:
    "returns a fake header"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Encoding": "identity",  # "gzip,deflate",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive": "115",
        "Connection": "keep-alive",
        "DNT": "1",
        "Referer": random.choice(REFERERS),
        "User-Agent": UA.random
    }
    return header


def static_header() -> dict:
    "returns a fake header"
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-us,en;q=0.5",
        "Accept-Encoding": ['gzip', 'deflate', 'sdch'],  # "gzip,deflate",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive": "115",
        "Connection": "keep-alive",
        "DNT": "1",
        "User-Agent": UA.Chrome
    }
    return header


def readable() -> dict:
    "for backward compatibility"
    return false_header()
