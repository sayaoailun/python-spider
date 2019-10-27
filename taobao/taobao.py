import sys, io, pprint, logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

fmt = '%(asctime)s %(pathname)s[line:%(lineno)d] %(module)s.%(funcName)s [%(processName)s/%(threadName)s] %(levelname)s : %(message)s'
# logging.basicConfig(handlers = [logging.FileHandler('log.txt', mode = 'w', encoding = 'utf-8')], level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('log.txt', mode='w', encoding='utf-8')], level=logging.INFO, format=fmt)

import requests, bs4, re, json, csv, threading, queue, time, random, openpyxl

threadPoolSize = 20
threadPool = queue.Queue()
bookQueue = queue.Queue()
threads = []

searchUrl = 'https://zhswts.tmall.com/search.htm?viewType=list&pageNo=%s'
asynSearchUrl = 'https://zhswts.tmall.com/i/asynSearch.htm?mid=w-16295071172-0&path=/search.htm&viewType=list&pageNo=%s'

headers = {}
headers['cookie'] = 'cna=anoJFO3WoWUCAd3dnGf6xGVn; _tb_token_=7e377e5e7be3e; cookie2=13c32bf8a5c2ceb9bb9b5f7ed352f9d2; tracknick=zhanglun33wei; ck1=""; lgc=zhanglun33wei; skt=df5da2f4ce4daa0f; whl=-1%260%260%260; dnk=zhanglun33wei; uc1=cookie16=V32FPkk%2FxXMk5UvIbNtImtMfJQ%3D%3D&cookie21=VFC%2FuZ9ajCNfDyoh%2B62%2BXw%3D%3D&cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=false&pas=0&cookie14=UoTbnxj5L5F8iw%3D%3D&tag=10&lng=zh_CN; uc3=nk2=GcAxdWUvzwTUqN3pjg%3D%3D&vt3=F8dByucgMVUTLhsXwhg%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&id2=UUkO1bkp8Lzc; lid=zhanglun33wei; uc4=id4=0%40U2uCuvcUXaZYJ39HXECrDPx5YQw%3D&nk4=0%40GwlAyxkf5xngaLeJNbEpQq5ktATwrax4; _l_g_=Ug%3D%3D; unb=210100158; cookie1=UUjTQ20awa7Oy0rlBa5y2Ar%2BMGrHU8SE678EiiyIEAU%3D; login=true; cookie17=UUkO1bkp8Lzc; _nk_=zhanglun33wei; t=c2eb478a4881d355937fc3367cbad854; sg=i81; csg=cc49355b; pnm_cku822=; cq=ccp%3D0; x5sec=7b2273686f7073797374656d3b32223a223633663635363063613835616534653761343134316666363964663664336437434f5336304f3046454a43707173484d39377a756c774561437a49784d4445774d4445314f44737a227d; l=dBQiuFYVqGZU-uGkBOCNCuI8Lt_T_IRAguPRwC2Mi_5Ir1T_zrQOkaI6re96cjWftMYB45113tv9-etkiepTY-fZtm7fRxDc.; isg=BIGB-XqduGSSqNRXyYE6P-sRkM1bBvSqK-IYNOPWZgjnyqGcK_xMcGzIqH4pQo3Y'
headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'

def getPageSize():
	response = requests.get('https://zhswts.tmall.com/i/asynSearch.htm?mid=w-16295071172-0&path=/search.htm&viewType=list&pageNo=1', headers = headers)
	response.raise_for_status()
	pageNum = 0
	pageSize = 0
	tag_bs = bs4.BeautifulSoup(response.text, 'html.parser').select('b')
	for b in tag_bs:
		if "/" in b.getText():
			pageNum = b.getText().split('/')[0]
			pageSize = b.getText().split('/')[1]
			break
	logging.info('pageNum = %s, pageSize = %s' % (pageNum, pageSize))
	return pageSize

def getOnePage(url):
	response = requests.get(url, headers = headers)
	response.raise_for_status()
	tag_as = bs4.BeautifulSoup(response.text, 'html.parser').select('dd > p > a')
	if len(tag_as) == 0:
		logging.info(response.text)
		raise Exception('error')
	items = []
	for a in tag_as:
		items.append(re.search(r'id=(.*?)&', a.get('href')).group(1))
	logging.info(items)
	return items

def getList():
	pageSize = getPageSize()
	allItems = []
	for x in range(1,int(pageSize)):
		items = getOnePage(asynSearchUrl % x)
		allItems = allItems + items
		logging.info(x)
		time.sleep(3)
	logging.info(allItems)
		

def getThread():
	while True:
		if threadPool.qsize() < threadPoolSize:
			break
		else:
			time.sleep(3)

if __name__ == '__main__':
	getList()