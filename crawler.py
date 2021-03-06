import sys
import time
import jieba
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
    
    #把課程cid找出來
    sql = "select * from course where courseName='%s'" % (courseName)
    cursor.execute(sql)
    cid = cursor.fetchone() 
    
    path = 'C:/xampp/htdocs/crawler/chromedriver.exe'
    driver = webdriver.Chrome(path)
    driver.get('https://www.dcard.tw/f/ncnu')
    
    #23~29: 控制搜尋引擎
    searchBar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div/div[1]/div/div/form/input'))
    )
    searchBtn = driver.find_element_by_xpath('//*[@id="__next"]/div[1]/div/div[1]/div/div/form/button')
    
    searchBar.send_keys(courseName)
    searchBtn.click()
    
    #等到網頁資料載入好再繼續動作
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div[1]/div[2]/article/h2/a'))
    )
    
    #51~69爬每篇文章的網址
    postsURL = []
    prev_ele = None
    for i in range(1,4):
        time.sleep(1)
        eles = driver.find_elements_by_class_name('sc-b205d8ae-0')
        # 若串列中存在上一次的最後一個元素，則擷取上一次的最後一個元素到當前最後一個元素進行爬取
        try:
            eles = eles[(eles.index(prev_ele)+1):]
        except:
            pass
        for ele in eles:
            try:
                href = ele.find_element_by_class_name('sc-b205d8ae-3').get_attribute('href')
                postsURL.append(href)
            except:
                pass
        if len(eles) == 0:
            pass
        else:
            prev_ele = eles[-1]
        js = "window.scrollTo(0, document.body.scrollHeight/4*" + str(i+1) + ");"
        driver.execute_script(js)
    
    #ua = UserAgent()
    #user_agent = ua.random
    #爬每篇文章的標題、內文、留言
    for i in postsURL:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, "html.parser")
        article = soup.find("h1").text
        contents = soup.find_all("div", class_="sc-8ec6ca7a-0")
        floor = soup.find_all("span", class_="sc-5ebd82a8-3")

        if (check_article_title(article, contents[0].text)):
            #填入文章標題、內文
            sql = "insert into article (cid,title,content) values (%d,'%s','%s')" % (cid[0], article, contents[0].text)
            cursor.execute(sql)
            db.commit()
            
            #將最新一筆資料的aid找出來
            sql = "select * from article order by aid desc limit 0,1"
            cursor.execute(sql)
            aid = cursor.fetchone()
            
            for i in range(1, len(contents)):
                sql = "insert into comment (aid,floor,comment) values (%d,'%s','%s')" % (aid[0], floor[i-1].get_text(), contents[i].text)
                cursor.execute(sql)
                db.commit()


# 查詢的課名 文章標題 文章內文
def check_article_title(tmpArticle, tmpContents):
    jieba.load_userdict("NOTdic.txt")

    Jieba_tmpArticle = []
    Jieba_tmpContents = []
    Jieba_tmpArticle.append((' '.join(jieba.cut(tmpArticle, cut_all=True, HMM=True))).split())
    Jieba_tmpContents.append((' '.join(jieba.cut(tmpContents, cut_all=True, HMM=True))).split())
    
    dataNOT = '換課 丟 交換禮物 周 週 禮拜 教室 送課 請假 衝堂 給離開同學的一封信 缺課 Warmpserver 資訊素養與倫理'
    Jieba_dataNOT = []
    Jieba_dataNOT.append((' '.join(jieba.cut(dataNOT, cut_all=True, HMM=True))).split())

    for i in range(0,len(Jieba_tmpArticle[0])) :    #找標題
        for j in range(0,len(Jieba_dataNOT[0])):
            if (Jieba_tmpArticle[0][i] == Jieba_dataNOT[0][j] and Jieba_dataNOT[0][j]!=' '):
                return False

    for i in range(0,len(Jieba_tmpContents[0])) :    #找內文
        for j in range(0,len(Jieba_dataNOT[0])):
            if (Jieba_tmpContents[0][i] == Jieba_dataNOT[0][j] and Jieba_dataNOT[0][j]!=' '):
                return False
    return True

def main():
    #courseName = input()
    courseName = sys.argv[1]  #要查詢的課名
    crawler(courseName)  #執行爬蟲
    db.close()

if __name__ == '__main__':
    main()