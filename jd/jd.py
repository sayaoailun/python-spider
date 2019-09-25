import logging
logging.basicConfig(handlers = [logging.FileHandler('log.txt', mode = 'w', encoding = 'utf-8')], level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')

import sys, io, pprint
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

import requests, bs4, re, json, csv

class Spider:
	def __init__(self, url, filename):
		self.url = url
		self.filename = filename
		self.books = []

	def save(self):
		self.bookList()
		file = open(self.filename, 'w', newline='')
		writer = csv.writer(file)
		writer.writerow(['排名', '书名', '价格', '定价', '作者', '出版社', 'ID', 'ISBN', '分类', '版次', '开本', '出版时间', '页数', '正文语种'])
		for book in self.books:
			writer.writerow([book['num'], book['name'], book['price'], book['m_price'], book['authors'], book['press'], book['id'], book['isbn'], book['class'], book['version'], book['size'], book['time'], book['page'], book['language']])
		file.close()

	def appendBook(self):
		self.bookList()
		file = open(self.filename, 'a', newline='')
		writer = csv.writer(file)
		for book in self.books:
			writer.writerow([book['num'], book['name'], book['price'], book['m_price'], book['authors'], book['press'], book['id'], book['isbn'], book['class'], book['version'], book['size'], book['time'], book['page'], book['language']])
		file.close()

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

	def tagList(self):
		response = requests.get(self.url)
		response.raise_for_status()
		soup = bs4.BeautifulSoup(response.content, 'html.parser')
		taglist = soup.select('ul[class="clearfix"] > li[clstag]')
		return taglist

	def bookInfo(self, bookTag):
		book = {}
		soup = bs4.BeautifulSoup(str(bookTag), 'html.parser')
		book['id'] = soup.select('em[data-price-id]')[0].get('data-price-id')
		book['num'] = soup.select('div[class="p-num"]')[0].getText()
		book['name'] = soup.select('a[class="p-name"]')[0].get('title').replace('\u3000', ' ')
		detail = soup.select('div[class="p-detail"] > dl')
		authors = []
		for author in bs4.BeautifulSoup(str(detail[0]), 'html.parser').select('dd > a'):
			authors.append(author.get('title'))
		book['authors'] = authors
		book['press'] = bs4.BeautifulSoup(str(detail[1]), 'html.parser').select('dd > a')[0].get('title')

		#获取 book price
		priceUrl = 'http://p.3.cn/prices/get?skuid=%s' % book['id']
		priceResponse = requests.get(priceUrl)
		priceResponse.raise_for_status()
		book['price'] = json.loads(priceResponse.text)[0].get('p')
		book['m_price'] = json.loads(priceResponse.text)[0].get('m')

		#获取 book ISBN等信息
		bookUrl = 'http://item.jd.com/%s.html' % book['id']
		bookResponse = requests.get(bookUrl)
		bookResponse.raise_for_status()
		bookResponse.encoding = 'gbk'
		for x in bs4.BeautifulSoup(bookResponse.text, 'html.parser').select('ul[id="parameter2"] > li'):
			if x.getText().find('ISBN') != -1:
				book['isbn'] = x.get('title')
				continue
			if x.getText().find('版次') != -1:
				book['version'] = x.get('title')
				continue
			if x.getText().find('开本') != -1:
				book['size'] = x.get('title')
				continue
			if x.getText().find('页数') != -1:
				book['page'] = x.get('title')
				continue
			if x.getText().find('出版时间') != -1:
				book['time'] = x.get('title')
				continue
			if x.getText().find('正文语种') != -1:
				book['language'] = x.get('title')
				continue
		self.fulfillBook(book)
		# 获取分类
		clazz = '图书'
		for x in bs4.BeautifulSoup(bookResponse.text, 'html.parser').select('div[class="crumb fl clearfix"] > div[class="item"] > a'):
			clazz += ('>' + x.getText())
		book['class'] = clazz
		return book

	def bookList(self):
		taglist = self.tagList()
		for tag in taglist:
			self.books.append(self.bookInfo(tag))
		return self.books

if __name__ == '__main__':
	spider = Spider('http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10002-1#comfort', 'jd图书销量榜.csv')
	spider.save()
	urlTemp = 'http://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10002-%s#comfort'
	for x in range(2,6):
		spider = Spider(urlTemp % x, 'jd图书销量榜.csv')
		spider.appendBook()