import urllib.request
import urllib.error
import threading
import os

import fake_useragent

UA = fake_useragent.UserAgent()


def new_header(agent = None, encoded = False):
	return {
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Accept-Language": "en-us,en;q=0.5",
		"Accept-Encoding": 'identity' if not encoded else 'gzip,deflate,sdch',
		"Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
		"Keep-Alive": "115",
		"Connection": "keep-alive",
		"DNT": "1",
		"Referer": '',
		"User-Agent": UA.random if not agent else agent
	}



def threaded(func):

	def run(*args, **kwds):
		new_thread = threading.Thread(
			target 	= func, 
			args 	= args, 
			kwargs 	= kwds)
		new_thread.start()
		return new_thread

	return run


def download(links, n_threads, encoded = False):
	"""
	links = [(link, path, name) for image in to_download]
	"""

	def make_path(path):
		if not os.path.exists(path):
			os.makedirs(path)

	def download_image(link, path, name):
		image = urllib.request.Request(
					link, 
					headers = new_header(encoded = encoded))
		data = urllib.request.urlopen(image).read()
		
		make_path(path)
		target = open(path + name, 'wb')
		target.write(data)
		target.close()

	def loop_download(link, path, name):
		try:
			download_image(link, path, name)
		except (ValueError, 
				urllib.error.HTTPError, 
				urllib.error.URLError):
			loop_download(link, path, name)

	@threaded
	def threaded_download(queue):
		next_image = next(queue, None)
		while next_image:
			loop_download(*next_image)
			next_image = next(queue, None)

	def main(links, n_threads):
		if encoded:
			raise NotImplementedError('encoding not yet supported')
		queue = iter(links)
		return [threaded_download(queue) for i in range(n_threads)]

	return main(links, n_threads)


link = 'https://docs.python.org/3/_static/py.png'
path = '/Users/Eight1911/Desktop/'
name = 'test_image.png'

queue = [(link, path, name)]
download(queue, 2, True)
