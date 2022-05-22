
from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import re
import csv
import pandas as pd

# ドライバーの設定
driver = webdriver.Chrome('chromedriver')

# netkeiba.comのレース詳細検索に移動
driver.get('https://db.netkeiba.com/?pid=race_search_detail')

# 検索条件のチェックボックスをクリック
# 芝
driver.find_element_by_xpath("//input[@id='check_track_1']").click()
# ダート
driver.find_element_by_xpath("//input[@id='check_track_2']").click()
# 東京
driver.find_element_by_xpath("//input[@id='check_Jyo_06']").click()
# 中山
driver.find_element_by_xpath("//input[@id='check_Jyo_07']").click()
# 中京
driver.find_element_by_xpath("//input[@id='check_Jyo_08']").click()
# 京都
driver.find_element_by_xpath("//input[@id='check_Jyo_09']").click()
# 阪神
driver.find_element_by_xpath("//input[@id='check_Jyo_10']").click()
# G1
driver.find_element_by_xpath("//input[@id='check_grade_1']").click()
# G2
driver.find_element_by_xpath("//input[@id='check_grade_2']").click()
# G3
driver.find_element_by_xpath("//input[@id='check_grade_3']").click()
#表示件数 = 100
Select(driver.find_element_by_id("db_search_detail_form").find_element_by_name("list")).select_by_value("20")

# 検索ボタンクリック
try:
    driver.find_element_by_css_selector("input[value='検索']").click()
except Exception:
    print('「検索」ボタンが押せませんでした')

sleep(1)

tableElem = driver.find_element_by_class_name("nk_tb_common.race_table_01")
trs = tableElem.find_elements(By.TAG_NAME, "tr")

search_lm = re.compile(r'(G1)|(G2)|(G3)')

urls = []
search_flag = FALSE

for i in range(1,len(trs)):
        tds = trs[i].find_elements(By.TAG_NAME, "td")
        for td in tds:
            atags = td.find_elements(By.TAG_NAME, "a")
            for atag in atags:
                if  bool(search_lm.search(atag.get_attribute("title"))):
                    urls.append(atag.get_attribute("href"))
                    search_flag = TRUE
                    break
            if search_flag == TRUE:
                search_flag = FALSE
                break

for url in urls:
    csv_data = []
    driver.get(url)
    racename = driver.find_element_by_class_name('racedata.fc').find_element_by_tag_name('h1')
    racedetail = driver.find_element_by_xpath("//*[@id='main']/div/div/div/diary_snap/div/div/dl/dd/p/diary_snap_cut/span")
    print("racedetail = ", racedetail.text)
    # dfs = pd.read_html(url)
    result_table = driver.find_element_by_class_name("race_table_01.nk_tb_common")
    trs = result_table.find_elements(By.TAG_NAME, "tr")
    for tr in trs:
        tr_data = []
        ths = tr.find_elements(By.TAG_NAME, "th")
        for th in ths:
            # print(th.text.strip())
            tr_data.append(th.text.replace('\n', ''))
        tds = tr.find_elements(By.TAG_NAME, "td")
        for td in tds:
            tr_data.append(td.text)
        # print("tr data = ", tr_data)
        if len(tr_data) != 0:
            csv_data.append(tr_data)
    df = pd.DataFrame(csv_data)
    # print("dataframe = " ,df)
    df.to_csv('./csv/test_' + racename.text + ".csv",header=False, index=False, encoding='shift-jis')
