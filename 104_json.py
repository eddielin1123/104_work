# encoding=utf-8
import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime
import jieba

keyword = '數據分析'
page = '1'
url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}'.format(keyword)
data = {'page': str(page)}
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
res = requests.get(url, headers=headers, params=data)
bs = BeautifulSoup(res.text, 'html.parser')
test = [a['href'] for a in bs.findAll('a', {'class': 'js-job-link'})]
json_url = []
url_para = []
for t in test:
    pattern = re.compile('[0-9].*\?')
    para_find = pattern.findall(t)
    json_url.append('https://www.104.com.tw/job/ajax/content/'+para_find[0].split('/')[2].split('?')[0])
    url_para.append(para_find[0].split('/')[2].split('?')[0])
for j,p in zip(json_url,url_para):
    referer = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Referer":"https://www.104.com.tw/job/"+p
    }
    enter_content = requests.get(j, headers=referer)
    json_data = json.loads(enter_content.text)
    print(json_data)