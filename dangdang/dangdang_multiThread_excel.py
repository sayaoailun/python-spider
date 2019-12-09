import sys, io, pprint, logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

fmt = '%(asctime)s %(pathname)s[line:%(lineno)d] %(module)s.%(funcName)s [%(processName)s/%(threadName)s] %(levelname)s : %(message)s'
# logging.basicConfig(handlers = [logging.FileHandler('log.txt', mode = 'w', encoding = 'utf-8')], level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('log.txt', mode='w', encoding='utf-8')], level=logging.INFO, format=fmt)

import os, requests, bs4, re, json, csv, threading, queue, time, random, openpyxl

threadPoolSize = 20
threadPool = queue.Queue()
bookQueue = queue.Queue()
threads = []

def getThread():
	while True:
		if threadPool.qsize() < threadPoolSize:
			break
		else:
			time.sleep(3)

class Spider:
	def __init__(self, url, filename):
		self.url = url
		self.filename = filename
		self.books = []
		self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
		self.proxies = {}
		self.proxies['http'] = 'http://10.126.3.161:56000'
		# self.headers = {}
		# self.headers['cache-control'] = 'max-age=0'
		# self.headers['upgrade-insecure-requests'] = '1'
		# self.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
		# self.headers['accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'
		# self.headers['accept-encoding'] = 'gzip, deflate'
		# self.headers['accept-language'] = 'zh-CN,zh;q=0.9'

	def save(self):
		self.bookList()
		file = open(self.filename, 'w', newline='')
		ff = open('book.txt', 'w', encoding = 'utf-8')
		writer = csv.writer(file)
		writer.writerow(['排名', '书名', '价格', '定价', '作者', '出版社', 'ID', 'ISBN', '分类', '版次', '开本', '出版时间', '页数', '正文语种'])
		for book in self.books:
			pprint.pprint(book, stream = ff)
			writer.writerow([book['num'], book['name'], book['price'], book['m_price'], book['authors'], book['press'], book['id'], book['isbn'], book['class'], book['version'], book['size'], book['time'], book['page'], book['language']])
		file.close()
		ff.close()

	def appendBook(self):
		self.bookList()
		file = open(self.filename, 'a', newline='')
		writer = csv.writer(file)
		ff = open('book.txt', 'a', encoding = 'utf-8')
		for book in self.books:
			pprint.pprint(book, stream = ff)
			writer.writerow([book['num'], book['name'], book['price'], book['m_price'], book['authors'], book['press'], book['id'], book['isbn'], book['class'], book['version'], book['size'], book['time'], book['page'], book['language']])
		file.close()
		ff.close()

	def fulfillBook(self, book):
		if book.get('version') == None:
			book['version'] = '-'
		if book.get('size') == None:
			book['size'] = '-'
		if book.get('page') == None:
			book['page'] = '-'
		if book.get('time') == None:
			book['time'] = '-'
		if book.get('language') == None:
			book['language'] = '-'
		if book.get('isbn') == None:
			book['isbn'] = '-'
		if book.get('class') == None:
			book['class'] = '-'

	def tagList(self):
		# 使用代理
		# response = requests.get(self.url, proxies = self.proxies, headers = self.headers)
		# 不使用代理
		UA = random.choice(self.user_agent_list)
		headers = {'User-Agent': UA}
		response = requests.get(self.url, headers = headers, allow_redirects = False)
		response.raise_for_status()
		if response.status_code == 302:
			return []
		else:
			response.encoding = 'gbk'
			soup = bs4.BeautifulSoup(response.text, 'html.parser')
			taglist = soup.select('ul[class="bang_list clearfix bang_list_mode"] > li')
			return taglist

	def bookInfo(self, bookTag):
		try:
			book = {}
			rank = bookTag.select('div[class="list_num red"]')
			if len(rank) == 0:
				rank = bookTag.select('div[class="list_num "]')
			book['num'] = rank[0].getText()[:-1]

			name = bookTag.select('div[class="name"] > a')
			book['name'] = name[0].get('title').replace('\u30fb', '·')

			publisher = bookTag.select('div[class="publisher_info"]')
			# book['authors'] = publisher[0].select('a')[0].get('title').replace('\u3000', ' ').replace('\u30fb', '·').replace('\u66da', '曚')
			if len(publisher[0].select('a')) == 0:
				book['authors'] = '-'
			else:
				book['authors'] = publisher[0].select('a')[0].get('title').replace('\u3000', ' ').replace('\ufffd', 'G')
			# book['authors'] = publisher[0].select('a')[0].get('title').replace('\u3000', ' ').replace('\ufffd', 'G')
			# book['press'] = publisher[1].select('a')[0].getText()
			if len(publisher[1].select('a')) == 0:
				book['press'] = '-'
			else:
				book['press'] = publisher[1].select('a')[0].getText()
			if len(publisher[1].select('span')) == 0:
				book['time'] = '-'
			else:
				book['time'] = publisher[1].select('span')[0].getText()

			book['price'] = bookTag.select('div[class="price"] > p > span[class="price_n"]')[0].getText().replace('\u00a5', '')
			# book['m_price'] = bookTag.select('div[class="price"] > p > span[class="price_r"]')[0].getText().replace('\u00a5', '')
			if len(bookTag.select('div[class="price"] > p > span[class="price_r"]')) == 0:
				book['m_price'] = '-'
			else:book['m_price'] = bookTag.select('div[class="price"] > p > span[class="price_r"]')[0].getText().replace('\u00a5', '')


			# 获取图书详情页信息
			bookurl = bookTag.select('div[class="pic"] > a')[0].get('href')
			book['url'] = bookurl
			book['id'] = bookurl[bookurl.find('.com/')+5:-5]
			# 使用代理
			# bookresponse = requests.get(bookurl, proxies = self.proxies, headers = self.headers)
			# 不使用代理
			UA = random.choice(self.user_agent_list)
			headers = {'User-Agent': UA}
			bookresponse = requests.get(bookurl, headers = headers)
			# bookresponse.raise_for_status()
			try:
				bookresponse.raise_for_status()
			except Exception as e:
				if bookresponse.status_code == 404:
					self.fulfillBook(book)
					bookQueue.put(book)
					threadPool.get()
					logging.info(book)
					return book
				else:
					raise e
			bookresponse.encoding = 'gbk'
			booksoup = bs4.BeautifulSoup(bookresponse.text, 'html.parser')
			bookcontent = booksoup.select('ul[class="key clearfix"] > li')
			for li in bookcontent:
				if 'ISBN' in li.getText():
					i = li.getText().find('ISBN')
					book['isbn'] = li.getText()[i+5:]
				if '开 本' in li.getText():
					i = li.getText().find('开 本')
					book['size'] = li.getText()[i+4:]

			self.fulfillBook(book)
			# 获取分类
			clazz = '图书'
			clazzes =bs4.BeautifulSoup(bookresponse.text, 'html.parser').select('div[class="breadcrumb"] > a')
			for x in range(1,clazzes.__len__()):
				clazz += ('>' + clazzes[x].getText())
			book['class'] = clazz
			bookQueue.put(book)
			threadPool.get()
			logging.info(book)
			return book
		except Exception as e:
			logging.exception(e)
			logging.info(bookTag)
			os._exit(1)
			# raise e
		

	def bookList(self):
		taglist = self.tagList()
		for tag in taglist:
			self.books.append(self.bookInfo(tag))
		return self.books

	def bookQueue(self):
		taglist = self.tagList()
		for tag in taglist:
			getThread()
			thread = threading.Thread(target = self.bookInfo, args = [tag])
			thread.start()
			threadPool.put(thread)
			threads.append(thread)
		return taglist

def write(sheetAndUrl, file):
	wb = openpyxl.Workbook()
	for sheet in sorted(sheetAndUrl):
		urlTemplate = sheetAndUrl[sheet]
		for x in range(1,6):
			spider = Spider(urlTemplate % x, sheet)
			if len(spider.bookQueue()) == 0:
				break
		for x in threads:
			x.join()
		bookDict = {}
		for x in range(bookQueue.qsize()):
			book = bookQueue.get()
			bookDict[book['num']] = book
		ws = wb.create_sheet(sheet)
		title = ['排名', '书名', '价格', '定价', '作者', '出版社', 'ID', 'ISBN', '分类', '版次', '开本', '出版时间', '页数', '正文语种']
		for x in range(1,len(title) + 1):
			c = ws.cell(row=1,column=x)
			c.value = title[x-1]
		for x in range(2,len(bookDict) + 2):
			book = bookDict['%s' % (x - 1)]
			content = [book['num'], book['name'], book['price'], book['m_price'], book['authors'], book['press'], book['id'], book['isbn'], book['class'], book['version'], book['size'], book['time'], book['page'], book['language']]
			for i in range(len(content)):
				c = ws.cell(row=x,column=i+1)
				c.value = content[i]
				if i == 1:
					c.style = 'Hyperlink'
					c.hyperlink = book['url']
	del wb['Sheet']
	wb.save(file)

if __name__ == '__main__':
	sheetAndUrl = {}
	sheetAndUrl['图书畅销榜'] = 'http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-%s'
	sheetAndUrl['小说图书畅销榜'] = 'http://bang.dangdang.com/books/bestsellers/01.03.00.00.00.00-recent7-0-0-1-%s'
	sheetAndUrl['文学图书畅销榜'] = 'http://bang.dangdang.com/books/bestsellers/01.05.00.00.00.00-recent7-0-0-1-%s'
	sheetAndUrl['外语图书畅销榜'] = 'http://bang.dangdang.com/books/bestsellers/01.45.00.00.00.00-recent7-0-0-1-%s'
	sheetAndUrl['英文原版图书畅销榜'] = 'http://bang.dangdang.com/books/bestsellers/01.58.00.00.00.00-recent7-0-0-1-%s'
	write(sheetAndUrl, 'dangdang.xlsx')