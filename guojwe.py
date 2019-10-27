import sys, io, pprint, logging
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

fmt = '%(asctime)s %(pathname)s[line:%(lineno)d] %(module)s.%(funcName)s [%(processName)s/%(threadName)s] %(levelname)s : %(message)s'
# logging.basicConfig(handlers = [logging.FileHandler('log.txt', mode = 'w', encoding = 'utf-8')], level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler('log.txt', mode='w', encoding='utf-8')], level=logging.INFO, format=fmt)

import requests, bs4, re, json, csv, threading, queue, time, random, openpyxl

raise Exception('hello')