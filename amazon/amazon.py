import logging
logging.basicConfig(handlers = [logging.FileHandler('log.txt', mode = 'w', encoding = 'utf-8')], level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

import sys, io, pprint
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

import requests, bs4, re, json, csv, random

class Spider:
	def __init__(self, url, filename):
		self.url = url
		self.amazonUrl = 'https://www.amazon.cn'
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

	def save(self):
		self.bookList()
		file = open(self.filename, 'w', newline='')
		writer = csv.writer(file)
		writer.writerow(['排名', '书名', '价格', '作者', '出版社', 'ASIN', '文件大小', '纸书页数', '语种', '品牌'])
		for book in self.books:
			# pprint.pprint(book)
			writer.writerow([book['num'], book['name'], book['price'], book['authors'], book['press'], book['asin'], book['size'], book['page'], book['language'], book['brand']])
		file.close()

	def appendBook(self):
		self.bookList()
		file = open(self.filename, 'a', newline='')
		writer = csv.writer(file)
		for book in self.books:
			# pprint.pprint(book)
			writer.writerow([book['num'], book['name'], book['price'], book['authors'], book['press'], book['asin'], book['size'], book['page'], book['language'], book['brand']])
		file.close()

	def fulfillBook(self, book):
		if book.get('brand') == None:
			book['brand'] = '-'
		if book.get('size') == None:
			book['size'] = '-'
		if book.get('page') == None:
			book['page'] = '-'
		if book.get('asin') == None:
			book['asin'] = '-'
		if book.get('language') == None:
			book['language'] = '-'
		if book.get('press') == None:
			book['press'] = '-'

	def tagList(self):
		UA = random.choice(self.user_agent_list)
		headers = {'User-Agent': UA}
		response = requests.get(self.url, headers = headers)
		response.raise_for_status()
		response.encoding = 'utf-8'
		soup = bs4.BeautifulSoup(response.text, 'html.parser')
		taglist = soup.select('div[class="a-section a-spacing-none aok-relative"]')
		return taglist

	def bookInfo(self, bookTag):
		book = {}
		soup = bs4.BeautifulSoup(str(bookTag), 'html.parser')
		book['url'] = soup.select('span[class="aok-inline-block zg-item"] > a[class="a-link-normal"]')[0].get('href')
		book['name'] = soup.select('span > div > img')[0].get("alt").replace('・', '·').replace('•', '·')
		# book['authors'] = soup.select('span[class="a-size-small a-color-base"]')[0].getText().replace('\x85', '...').replace('•', '·')
		book['price'] = soup.select('span[class="p13n-sc-price"]')[0].getText().replace('￥', '')
		book['num'] = soup.select('span[class="zg-badge-text"]')[0].getText().replace('#', '')

		# 获取书籍详情
		UA = random.choice(self.user_agent_list)
		headers = {'User-Agent': UA}
		response = requests.get(self.amazonUrl + book['url'], headers = headers)
		response.raise_for_status()
		response.encoding = 'utf-8'
		soup = bs4.BeautifulSoup(response.text, 'html.parser')
		book['authors'] = soup.select('div[class="a-section a-spacing-micro bylineHidden feature"]')[0].getText().replace('\n', '').replace('・', '·').replace('•', '·')
		litags = soup.select('div[class="content"] > ul > li')
		for li in litags:
			if li.select('b').__len__() == 0:
				continue
			if li.select('b')[0].getText().find('文件大小：') != -1:
				book['size'] = li.getText()[5:]
				continue
			if li.select('b')[0].getText().find('纸书页数：') != -1:
				book['page'] = li.getText()[5:]
				continue
			if li.select('b')[0].getText().find('出版社:') != -1:
				book['press'] = li.getText()[4:]
				continue
			if li.select('b')[0].getText().find('语种：') != -1:
				book['language'] = li.getText()[3:]
				continue
			if li.select('b')[0].getText().find('ASIN:') != -1:
				book['asin'] = li.getText()[5:]
				continue
			if li.select('b')[0].getText().find('品牌:') != -1:
				book['brand'] = li.getText()[3:].replace('・', '·').replace('•', '·')
				continue
		self.fulfillBook(book)
		return book

	def bookList(self):
		taglist = self.tagList()
		for tag in taglist:
			self.books.append(self.bookInfo(tag))
		return self.books

if __name__ == '__main__':
	spider = Spider('https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=zg_bs', 'amazon付费.csv')
	spider.save()
	spider = Spider('https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=zg_bs_pg_2?ie=UTF8&pg=2', 'amazon付费.csv')
	spider.appendBook()
	spider = Spider('https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=zg_bs?ie=UTF8&tf=1', 'amazon免费.csv')
	spider.save()
	spider = Spider('https://www.amazon.cn/gp/bestsellers/digital-text/116169071/ref=zg_bs_pg_2?ie=UTF8&pg=2&tf=1', 'amazon免费.csv')
	spider.appendBook()
	