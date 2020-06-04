# encoding=utf-8
import requests
import json
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from datetime import datetime
import os

def search_104_tocsv(word, total_page):
    page = 1
    COMPANY = [];
    JOB = [];
    JOB_CONTENT = [];
    JOB_REQUIRE = [];
    JOB_WELFARE = [];
    JOB_CONTACT = [];
    JOB_URL = []
    python = [];
    java = [];
    javascript = [];
    r_language = [];
    mysql = [];
    mongodb = [];
    nosql = [];
    sql = [];
    aws = [];
    gcp = [];
    azure = []
    data_mining = [];
    ai = [];
    deep_learning = [];
    cloud_service = []
    while page <= total_page:
        url = 'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&order=12&asc=0&page=2&mode=s&jobsource=2018indexpoc'.format(word)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        data = {
            'page': str(page)
        }
        res = requests.get(url, headers=headers, params=data)
        bs = BeautifulSoup(res.text, 'html.parser')
        bs_title = bs.findAll('article', {'class': 'b-block--top-bord job-list-item b-clearfix js-job-item'})
        for a in bs_title:
            # #     # print('職稱:',a['data-job-name'])
            # print('公司名稱:', a['data-cust-name'])
            # print('職缺:', a.find('a', {'class': 'js-job-link'}).text)
            title_url = 'https:' + a.find('a')['href']
            # print('職缺URL:', title_url)
            # 正則解取網頁參數並代入網址
            pattern = re.compile('[0-9].*\?')
            get_data = pattern.findall(title_url)[0].split('/')[2].split('?')[0]
            referer = 'https://www.104.com.tw/job/' + get_data
            json_url = 'https://www.104.com.tw/job/ajax/content/' + get_data
            title_headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                "Referer": "https://www.104.com.tw/job/{}".format(get_data)
            }
            # 讀取網頁json檔
            enter_content = requests.get(json_url, headers=title_headers)
            json_data = json.loads(enter_content.text)
            # 工作內容
            job_desciption = '工作內容:' + '\n' + json_data['data']['jobDetail']['jobDescription']
            # 職務類別
            job_category_str = '職務類別:'
            job_category = json_data['data']['jobDetail']['jobCategory']
            # print(job_category)
            for j in job_category:
                job_category_str += j['description'] + '\t'
            # print(job_category_str)
            # 工作待遇
            job_salary = '工作待遇: ' + json_data['data']['jobDetail']['salary']
            # 工作性質
            job_attr = json_data['data']['jobDetail']['jobType']
            if job_attr == 1:
                job_attr = '工作性質: 全職'
            elif job_attr == 2:
                job_attr = '工作性質: 兼職'
            # 上班地點
            job_loc = '上班地點: ' + json_data['data']['jobDetail']['addressRegion'] + json_data['data']['jobDetail'][
                'addressDetail']
            # 管理責任
            job_resp = '管理責任: ' + json_data['data']['jobDetail']['manageResp']
            # 出差外派
            job_btrip = '出差外派: ' + json_data['data']['jobDetail']['businessTrip']
            # 上班時段
            job_peri = '上班時段: ' + json_data['data']['jobDetail']['workPeriod']
            # 休假制度
            job_vac = '休假制度: ' + json_data['data']['jobDetail']['vacationPolicy']
            # 可上班日
            job_star = '可上班日: ' + json_data['data']['jobDetail']['startWorkingDay']
            # 需求人數
            job_need = '需求人數: ' + json_data['data']['jobDetail']['needEmp']
            # 完整工作內容
            full_content = job_desciption + \
                           '\n' + job_category_str + '\n' + job_salary + '\n' + job_attr + '\n' + job_loc + '\n' + \
                           job_resp + '\n' + job_btrip + '\n' + job_peri + '\n' + job_vac + '\n' + job_star + '\n' + job_need
            # 接受身分
            require_role = '接受身分: ' + json_data['data']['condition']['acceptRole']['role'][0]['description']
            # 工作經歷
            require_workExp = '工作經歷: ' + json_data['data']['condition']['workExp']
            # 學歷要求
            require_edu = '學歷要求: ' + json_data['data']['condition']['edu']
            # 科系要求
            require_maj = '科系要求: ' + '、'.join(json_data['data']['condition']['major'])
            # 語文條件
            try:
                require_lan = '語文條件: ' + json_data['data']['condition']['language'][0]['language'] + \
                              json_data['data']['condition']['language'][0]['ability']
            except IndexError:
                require_lan = '語文條件: 不拘'
            # 擅長工具
            try:
                require_specialty = '擅長工具: ' + str(json_data['data']['condition']['specialty'][0]['description'])
            except IndexError:
                require_specialty = '擅長工具: 不拘'
            # 工作技能
            try:
                require_skill = '工作技能: ' + str(json_data['data']['condition']['skill'][0]['description'])
            except IndexError:
                require_skill = '工作技能: 不拘'
            # 其他條件
            require_other = '其他條件: ' + json_data['data']['condition']['other']
            # 福利制度
            welfare = '福利制度: ' + json_data['data']['welfare']['welfare']
            # 聯絡方式
            contact = '聯絡方式: ' + json_data['data']['contact']['hrName'] + '\n' + json_data['data']['contact'][
                'email'] + '\n' + json_data['data']['contact']['phone']
            full_require = require_role + '\n' + require_workExp + '\n' + require_edu + '\n' + require_maj + '\n' + require_lan + '\n' + \
                           require_specialty + '\n' + require_skill + '\n' + require_other
            COMPANY.append(a['data-cust-name'])
            JOB.append(a.find('a', {'class': 'js-job-link'}).text)
            JOB_CONTENT.append(full_content)
            JOB_REQUIRE.append(full_require)
            JOB_WELFARE.append(welfare)
            JOB_CONTACT.append(contact)
            JOB_URL.append(title_url)
            print('')
            if 'python' in full_content and require_specialty:
                python.append(1)
            else:
                python.append(0)
            if 'java' in full_content and require_specialty:
                java.append(1)
            else:
                java.append(0)
            if 'javascript' in full_content and require_specialty:
                javascript.append(1)
            else:
                javascript.append(0)
            if 'r語言' or 'R語言' in full_content and require_specialty:
                r_language.append(1)
            else:
                r_language.append(0)
            if 'MySQL' or 'MYSQL' in full_content and require_specialty:
                mysql.append(1)
            else:
                mysql.append(0)
            if 'mongodb' or 'MongoDB' in full_content and require_specialty:
                mongodb.append(1)
            else:
                mongodb.append(0)
            if 'NoSQL' or 'NOSQL' or 'No SQL' in full_content and require_specialty:
                nosql.append(1)
            else:
                nosql.append(0)
            sql_filter = re.compile('^(SQL|sql)$')
            if 'sql' or 'SQL' in sql_filter.findall(full_content) and sql_filter.findall(require_specialty):
                sql.append(1)
            else:
                sql.append(0)
            if 'aws' or 'AWS' in full_content and require_specialty:
                aws.append(1)
            else:
                aws.append(0)
            if 'gcp' or 'GCP' in full_content and require_specialty:
                gcp.append(1)
            else:
                gcp.append(0)
            if 'azure' or 'AZURE' in full_content and require_specialty:
                azure.append(1)
            else:
                azure.append(0)
            if 'data mining' in full_content.lower() and require_specialty.lower():
                data_mining.append(1)
            else:
                data_mining.append(0)
            if 'ai' or '人工智慧' or '人工智慧' in full_content.lower() and require_specialty.lower():
                ai.append(1)
            else:
                ai.append(0)
            if 'deep learning' or '深度學習' in full_content.lower() and require_specialty.lower():
                deep_learning.append(1)
            else:
                deep_learning.append(0)
            if 'cloud service' or '雲端服務' or '雲服務' in full_content.lower() and require_specialty.lower():
                cloud_service.append(1)
            else:
                cloud_service.append(0)
        page += 1
    dict = {'Job_compay': COMPANY, 'Job Openings': JOB, 'Job_contetn': JOB_CONTENT, 'Job require': JOB_REQUIRE,
            'Job welfare': JOB_WELFARE, 'Job contact': JOB_CONTACT, 'URL': JOB_URL, 'python': python, 'java': java,
            'javascript': javascript, 'r語言': r_language, 'mysql': mysql, 'mongodb': mongodb, 'nosql': mongodb,
            'sql': sql, 'aws': aws, 'gcp': gcp, 'azure': azure, 'data mining': data_mining, 'ai': ai,
            'deep learning': deep_learning, 'cloud service': cloud_service}
    df = pd.DataFrame(dict)
    print('總共擷取{}個結果'.format(len(JOB_URL)))
    return df
    # print(len(python),len(java),len(javascript),len(r_language),len(mysql),len(mongodb),len(nosql),len(sql),len(aws),len(gcp),len(azure),len(data_mining),len(ai),len(deep_learning),len(cloud_service))
    # print(len(COMPANY),len(JOB),len(JOB_CONTENT),len(JOB_REQUIRE),len(JOB_CONTACT),len(JOB_WELFARE),len(JOB_URL))

def main():
    start_time = datetime.now()
    word = sys.argv[1]
    page = sys.argv[2]
    search_104_tocsv(str(word),int(page)).to_csv('./104_search_result.csv')
    end_time = datetime.now()
    total_time = end_time-start_time

    print('總共花了',total_time.seconds,'秒')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('使用方法： ETL_104work 搜尋字串 總擷取頁數')
    else:
        main()