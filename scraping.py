# RaceIDの決め方
# yyyymmddccRR

# yyyy=開催年（西暦）
# mm=開催月(2桁)
# dd = 開催日(2桁)
# cc = コース
# 札幌=01　函館=02　福島=03　新潟=04　東京=05　中山=06　中京=07　京都=08　阪神=09　小倉=10　
# RR = レース
# 2022/5/29 東京 第2レースの場合: ID = 202205290502


from asyncio.windows_events import NULL
from cgitb import text
from cmath import asin
from pickle import FALSE, TRUE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import re
import csv
import pandas as pd

COURCE_ID = {"札幌":"01","函館":"02","福島":"03","新潟":"04","東京":"05","中山":"06","中京":"07","京都":"08","阪神":"09","小倉":"10"}

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
# # G1
# driver.find_element_by_xpath("//input[@id='check_grade_1']").click()
# # G2
# driver.find_element_by_xpath("//input[@id='check_grade_2']").click()
# # G3
# driver.find_element_by_xpath("//input[@id='check_grade_3']").click()
表示件数 = 100
Select(driver.find_element_by_id("db_search_detail_form").find_element_by_name("list")).select_by_value("20")

# 検索ボタンクリック
try:
    driver.find_element_by_css_selector("input[value='検索']").click()
except Exception:
    print('「検索」ボタンが押せませんでした')

sleep(1)

# 検索結果テーブルの指定
tableElem = driver.find_element_by_class_name("nk_tb_common.race_table_01")
# 各テーブルの行要素抽出
trs = tableElem.find_elements(By.TAG_NAME, "tr")
# 重賞検知用モジュール
search_lm = re.compile(r'(G1)|(G2)|(G3)')

urls = []
search_flag = FALSE
# //*[@id="contents_liquid"]/table/tbody/tr[2]/td[5]
for i in range(1,len(trs)):
        tds = trs[i].find_elements(By.TAG_NAME, "td")
        atag = tds[4].find_element(By.TAG_NAME, "a")
        urls.append(atag.get_attribute("href"))
        search_flag = TRUE
        if search_flag == TRUE:
            search_flag = FALSE
            # URL取得済みなら検索結果テーブルの次の行へ

for url in urls:
    csv_data = []
    driver.get(url)
    # レース名取得
    racename = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/diary_snap/div/div/dl/dd/h1').text
    # レース詳細取得
    racedetail = driver.find_element_by_xpath("//*[@id='main']/div/div/div/diary_snap/div/div/dl/dd/p/diary_snap_cut/span").text.split('/')

    # 芝/ダート情報取得
    field = '-'
    if '芝' in racedetail[0]:
        field = '芝'
    elif 'ダ' in racedetail[0]:
        field = 'ダート'
    # 右回り/左回り
    rl_round = '-'
    if '右' in racedetail[0]:
        rl_round = '右'
    elif '左' in racedetail[0]:
        rl_round = '左'
    # 距離情報
    dist = re.sub(r"\D", "", racedetail[0])
    # 天候
    weather = racedetail[1].split(':')[1]
    # 馬場状態
    g_state = racedetail[2].split(':')[1]
    # 第何レースか
    race_no = re.sub(r"\D", "", driver.find_element_by_xpath('//*[@id="main"]/div/div/div/diary_snap/div/div/dl/dt').text).zfill(2)
    raceid = ""
    racedetail_2 = driver.find_element_by_xpath('//*[@id="main"]/div/div/div/diary_snap/div/div/p').text.split()
    date_buf = re.split('[年月日]', racedetail_2[0])
    race_year = date_buf[0].zfill(2)
    race_month = date_buf[1].zfill(2)
    race_date = date_buf[2].zfill(2)
    race_cource_id = "00"
    race_cource_name = ""
    for cource_name in COURCE_ID.keys():
        if cource_name in racedetail_2[1]:
            race_cource_id = COURCE_ID[cource_name]
            race_cource_name = cource_name
    raceid = race_year + race_month + race_date + race_cource_id + race_no

    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    # print(racename)
    # print("raceID = ", raceid)
    # print(race_year, "年")
    # print(race_month, "月")
    # print(race_date, "日")
    # print(race_cource_name)
    # print(race_no, "レース")
    # print(field)
    # print(rl_round,"周り")
    # print(dist, "m")
    # print("天候：", weather)
    # print("馬場：", g_state)
    # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    # print("racedetail = ", racedetail)
    # dfs = pd.read_html(url)
    # race_year
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
    
    df = df.drop(df.columns[[9, 16, 17, 18]], axis=1)
    print("dataframe = " ,df)

    df.to_csv('./csv/test_' + racename + ".csv",header=False, index=False)
