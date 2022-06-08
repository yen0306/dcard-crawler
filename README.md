# dcard-crawler
- 從dcard爬取課程文章內容及留言，做成可依課名搜尋課程相關問題和評論的網站
## 要安裝的套件
```shell=
pip install jieba
```
```shell=
pip install pymysql
```
```shell=
pip install selenium
```
```shell=
pip install BeautifulSoup
```
## 檔案說明
- crawler.py:
  - 爬蟲+結巴
- searchUI.html:
  - 搜尋介面
- showUI.html:
  - 展示結果介面
