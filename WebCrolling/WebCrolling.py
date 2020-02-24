from selenium import webdriver
from urllib.request import urlretrieve
import os
import urllib
import time

url = input("사이트 주소 입력 후 엔터")
path = input("저장할 폴더 경로 입력 후 엔터 (예시) D:\GOLDENCHILD")

# 웹 접속
print("접속중")
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(20)

driver.get(url)

imgs = driver.find_elements_by_css_selector('div > div > div > div > div.se_viewArea > a')
imgs2 = driver.find_elements_by_css_selector('div > div > div > div > div.se_imageStripArea > a')
title = driver.find_element_by_css_selector('h3.se_textarea').text
date = driver.find_element_by_css_selector('span.se_publishDate').text

result = []
for a in imgs:
    urll = a.get_attribute('data-linkdata')
    urll1 = urll.find('http')
    urll2 = urll.rfind('", "linkUse"')
    urll = urll[urll1:urll2]
    if '?type=w1200' in urll:
        urll3 = urll.find('?type=w1200')
        urll = urll[:urll3]
        print(urll)
    else:
        print(urll)
    result.append(urll)
for a in imgs2:
    urll = a.get_attribute('data-linkdata')
    urll1 = urll.find('http')
    urll2 = urll.rfind('", "linkUse" : "false", "link" : ""}')
    urll = urll[urll1:urll2]
    if '?type=w1200' in urll:
        urll3 = urll.find('?type=w1200')
        urll = urll[:urll3]
        print(urll)
    else:
        print(urll)
    result.append(urll)

driver.close()
print("수집완료")

# 폴더명 정의
datename = date.split(".")
datename = "".join(datename)[2:8]

# 폴더생성
if not os.path.isdir('{}/{}'.format(path, datename)):
    os.mkdir('{}/{}'.format(path, datename))
print('폴더명: ' + datename)

# 이미지링크
for index, link in enumerate(result):
    if 'post-phinf.pstatic' in link:
        start = link.rfind('.')
        if '"' in link:
            end = link.find('"')
            filetype = link[start:end]
        else:
            filetype = link[start:]
        namestart = link.rfind('/')
        nameend = link.rfind('.')
        name = link[namestart:nameend]
        name = urllib.parse.unquote(name)
        print(name + filetype)

        urlretrieve(link, '{}/{}/{}{}'.format(path, datename, name, filetype))

print("다운로드 완료")
