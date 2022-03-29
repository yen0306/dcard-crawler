# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 16:44:07 2022

@author: User
"""

import time
import pymysql
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#連線資料庫
db = pymysql.connect(host='localhost', user='root', passwd='', db='test')
cursor = db.cursor()

def crawler(courseName):
    #填入課程名稱
    sql = "insert into course (courseName) values ('%s')" % (courseName)
    cursor.execute(sql)
    db.commit()
    
    #把課程id找出來
    sql = "select * from course where courseName='%s'" % (courseName)
    cursor.execute(sql)
    cid = cursor.fetchone() 
    
    path = 'C:/xampp/htdocs/crawler/chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.get('https://www.dcard.tw/f/ncnu')
    
    #23~29: 控制搜尋引擎
    searchBar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "query"))
    )
    searchBtn = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div[1]/div/div/form/button')
    
    searchBar.send_keys(courseName)
    searchBtn.click()
    
    #等到網頁資料載入好再繼續動作
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[2]/article/h2/a'))
    )
    
    postsURL = []
    prev_ele = None
    for i in range(1,4):
        time.sleep(1)
        eles = driver.find_elements_by_class_name('tgn9uw-0')
        # 若串列中存在上一次的最後一個元素，則擷取上一次的最後一個元素到當前最後一個元素進行爬取
        try:
            eles = eles[(eles.index(prev_ele)+1):]
        except:
            pass
        for ele in eles:
            try:
                href = ele.find_element_by_class_name('tgn9uw-3').get_attribute('href')
                postsURL.append(href)
            except:
                pass
        prev_ele = eles[-1]
        js = "window.scrollTo(0, document.body.scrollHeight/4*" + str(i+1) + ");"
        driver.execute_script(js)
    
    #爬每篇文章的標題、內文、留言
    for i in postsURL:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("h1").text
        contents = soup.find_all("div", class_="phqjxq-0")
        
        #填入文章標題、內文
        sql = "insert into article (cid,title,content) values (%d,'%s','%s')" % (cid[0], article, contents[0].text)
        cursor.execute(sql)
        db.commit()
        
        #將最新一筆資料的id找出來
        sql = "select * from article order by id desc limit 0,1"
        cursor.execute(sql)
        aid = cursor.fetchone()
        
        #填入該篇文章的所有留言
        for i in range(1, len(contents)):
            sql = "insert into comment (aid,comment) values (%d,'%s')" % (aid[0], contents[i].text)
            cursor.execute(sql)
            db.commit()

def main():
    courseName = str(input()) #輸入要查詢的課名
    
    #找出課程資訊
    sql = "select count(*) from course where courseName='%s'" % (courseName)
    cursor.execute(sql)
    result = cursor.fetchone()
    
    #如果沒有課程資訊就執行爬蟲
    if result[0] == 0:
        crawler(courseName)
    else:
        print("已有資料")
    
    db.close()

if __name__ == '__main__':
    main()


