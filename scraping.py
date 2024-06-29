from logging import exception
from telnetlib import EC
from pickle import FALSE, TRUE
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from time import sleep
import re
import csv
import pandas as pd
import os
import glob
import subprocess
import Selfmade_functions as Smf

class Browser:
    def scrollByElemAndOffset(self, element, offset = 0):

        self.driver.execute_script("arguments[0].scrollIntoView();", element)

        if (offset != 0):
            script = "window.scrollTo(0, window.pageYOffset + " + str(offset) + ");"
            self.driver.execute_script(script)

RACE_COURCE = { 
    '01':'札幌',
    '02':'函館',
    '03':'福島',
    '04':'新潟',
    '05':'東京',
    '06':'中山',
    '07':'中京',
    '08':'京都',
    '09':'阪神',
    '10':'小倉'
}

def Url_scraping(url, driver):
    raceid = url.rsplit('/', 2)[-2]
    # レース情報格納用のdict(作成兼初期化)
    racedetail_dict = {
        'year': '-', # 開催年
        'month': '-', # 開催月
        'date': '-', # 開催日
        'cource': '-', # レース場
        'dist': 0, #距離
        'weather': '-', # 天候
        'ground': '-', #芝ダート
        'g_state': '-', #馬場
        'around': '-' # 左右回り
        }
    
    racedetail_dict['cource'] = RACE_COURCE[raceid[4:6]]
    csv_data = []
    driver.get(url)
    # レース名取得
    # //*[@id="main"]/div/div/div/diary_snap/div/div/dl/dd/h1/text()
    racename = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/diary_snap/div/div/dl/dd/h1').text
    # レース開催日時取得
    # （例）2022年6月5日 3回東京2日目 3歳以上オープン  (国際)(指)(定量)
    racedate = driver.find_element(By.XPATH, '//*[@id="main"]/div/div/div/diary_snap/div/div/p').text
    racedate = re.findall(r'\d+', racedate)[:3]
    racedetail_dict['year'] = racedate[0]
    racedetail_dict['month'] = racedate[1]
    racedetail_dict['date'] = racedate[2]
    # レース詳細取得
    # (例) 芝左1200m / 天候 : 晴 / 芝 : 良 / 発走 : 15:35
    racedetail = driver.find_element(By.XPATH, "//*[@id='main']/div/div/div/diary_snap/div/div/dl/dd/p/diary_snap_cut/span")
    racedetail = racedetail.text
    racedetail_list = racedetail.split(r'/')
    # 芝ダート情報登録
    if '芝' in racedetail_list[0]:
        racedetail_dict['ground'] = '芝'
    elif 'ダ' in racedetail_list[0]:
        racedetail_dict['ground'] = 'ダート'
    # 回り向き情報登録
    if '右' in racedetail_list[0]:
        racedetail_dict['around'] = '右'
    elif '左' in racedetail_list[0]:
        racedetail_dict['around'] = '左'
    # 距離登録
    racedetail_dict['dist'] = re.sub(r'\D', '', re.findall(r'\d.*m', racedetail)[0])
    # 天候登録
    racedetail_dict['weather'] = racedetail_list[1].split(':')[1]
    # 馬場状態登録
    racedetail_dict['g_state'] = racedetail_list[2].split(':')[1]

    # レース結果テーブル取得
    result_table = driver.find_element(By.XPATH, '//*[@id="contents_liquid"]/table')
    trs = result_table.find_elements(By.TAG_NAME, "tr")
    # 行ごとに操作
    hource_ids =[]
    for tr in trs:
        tr_data = []
        ths = tr.find_elements(By.TAG_NAME, "th")
        # 行内のセルごとに取得
        for th in ths:
            # print(th.text.strip())
            tr_data.append(th.text.replace('\n', ''))
        tds = tr.find_elements(By.TAG_NAME, "td")
        for td in tds:
            tr_data.append(td.text)
            # 馬のid取得
            try:
                if bool(re.search('umalink', td.find_element(By.TAG_NAME, "a").get_attribute('id'))):
                    hource_id = td.find_element(By.TAG_NAME, "a").get_attribute('href').split(r'/')[-2]
                    hource_ids.append(hource_id)
            except:
                None
        # print("tr data = ", tr_data)
        if len(tr_data) != 0:
            csv_data.append(tr_data)
    df = pd.DataFrame(csv_data[1:], columns=csv_data[0])
    # print("dataframe = " ,df)
    # いらない列の削除
    droplist=['ﾀｲﾑ指数', '調教ﾀｲﾑ', '厩舎ｺﾒﾝﾄ','備考']
    for dropcol in droplist:
        try:
            df = df.drop(df.filter(like = dropcol, axis=1), axis=1)
        except:
            # なかったらスキップ
            None
    
    # すべての要素の両端の空白削除
    for key in racedetail_dict.keys():
        racedetail_dict[key] = racedetail_dict[key].strip()

    # 各種成形
    df['race_name'] = racename
    df['raceID'] = raceid
    df['cource'] = racedetail_dict['cource']
    df['distance'] = racedetail_dict['dist']
    df['around'] = racedetail_dict['around']
    df['groung'] = racedetail_dict['ground']
    df['groung_state'] = racedetail_dict['g_state'].replace(' ', '')
    
    df['weather'] = racedetail_dict['weather'].replace(' ', '')
    df['houceID'] = hource_ids
    # 性齢 = 牡4みたいな感じなので分ける
    df['sex'] = df['性齢'].str[0]
    df['age'] = df['性齢'].str[1]
    df = df.drop('性齢', axis=1) #元の列は削除
    
    #馬体重 = 446(-2)みたいな感じなので、446, -2という感じに分ける
    s_org = df['馬体重'].str.extract('(.*)\((.*)\)', expand = True)
    df['hource_weight'] = s_org[0]
    df['weight_diff'] = s_org[1]
    df = df.drop('馬体重', axis=1)
    # df['馬体重'] = df['馬体重'].str.extract("(?<=\().+?(?=\))")
    return df

def All_cource_scraping():

    # 保存用フォルダ作成
    os.makedirs(os.path.dirname(__file__)+'/csv', exist_ok=True)
    SAVE_DIR = './csv/'

    # 保存済みのレースidリスト取得(重複取得の回避)
    csvs_path = glob.glob(os.path.join(SAVE_DIR,'*.csv'))
    SCRAPED_LIST = [os.path.basename(f) for f in csvs_path]

    # print(SCRAPED_LIST)
    # os.abort()

    # ドライバーの設定
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # netkeiba.comのレース詳細検索に移動
    driver.get('https://db.netkeiba.com/?pid=race_search_detail')
    # find_element(by=By.XPATH, value=xpath)

    # 検索条件のチェックボックスをクリック
    # 芝
    # driver.find_element_by_xpath("//input[@id='check_track_1']").click()
    driver.find_element(By.XPATH, '//*[@id="check_track_1"]').click()
    # ダート
    driver.find_element(By.XPATH,"//input[@id='check_track_2']").click()

    # 期間
    # 開始年
    pulldown = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/form/table/tbody/tr[3]/td/select[1]")
    select = Select(pulldown)
    select.select_by_value('2000')

    # 終了年
    # pulldown = driver.find_element(By.XPATH,"/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/form/table/tbody/tr[3]/td/select[3]")
    # select = Select(pulldown)
    # select.select_by_value('2010')

    # 東京
    driver.find_element(By.XPATH,"//input[@id='check_Jyo_06']").click()
    # 中山
    driver.find_element(By.XPATH,"//input[@id='check_Jyo_07']").click()
    # 中京
    driver.find_element(By.XPATH,"//input[@id='check_Jyo_08']").click()
    # 京都
    driver.find_element(By.XPATH,"//input[@id='check_Jyo_09']").click()
    # 阪神
    driver.find_element(By.XPATH,"//input[@id='check_Jyo_10']").click()
    # # G1
    # driver.find_element(By.XPATH,"//input[@id='check_grade_1']").click()
    # # G2
    # driver.find_element(By.XPATH,"//input[@id='check_grade_2']").click()
    # # G3
    # driver.find_element(By.XPATH,"//input[@id='check_grade_3']").click()
    #表示件数 = 20
    Select(driver.find_element(By.XPATH, '//*[@id="db_search_detail_form"]/form/table/tbody/tr[11]/td/select')).select_by_value("20")
    #検索ボタンを探す
   

    # 検索ボタンクリック
    try:
        forserch_elem = driver.find_element(By.XPATH, '//*[@id="db_search_detail_form"]/form/div/input[1]')
        driver.execute_script("arguments[0].scrollIntoView();", forserch_elem)
        sleep(1)
        forserch_elem.click()
        # driver.find_element_by_css_selector("input[value='検索']").click()
    except ElementClickInterceptedException as e:
        print(f"要素がクリックできませんでした: {e}")
    except ElementNotInteractableException as e:
        print(f"要素がインタラクティブでないためクリックできませんでした: {e}")
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
    finally:
        # ブラウザを閉じる
        driver.quit()

    search_lm = re.compile(r'(G1)|(G2)|(G3)')


    while True:
        # 表の情報取得
        tableElem = driver.find_element(By.XPATH, '//*[@id="contents_liquid"]/table')
        trs = tableElem.find_elements(By.TAG_NAME, "tr")
        # URL取得
        urls = []
        for i in range(1,len(trs)):
            # 検索結果表の各行5列目(レース名)のURLを取得
            tds = trs[i].find_elements(By.TAG_NAME, "td")
            atag = tds[4].find_element(By.TAG_NAME, "a")
            urls.append(atag.get_attribute("href"))

        # 検索結果の次のページを表示
        try:
            nextpage = driver.find_element(By.XPATH, '//html/body/div[1]/div[2]/div[2]/ul[1]/li[14]/a').get_attribute("href")
            print('nextpage exested')
        except:
            # 次のページが取得できない=検索結果最後のページ
            nextpage = None
            print('last page')


        # 各レース先にアクセス
        for url in urls:
            raceid = url.rsplit('/', 2)[-2]
            # 取得済みレースの場合スキップ
            if raceid + '.csv' in SCRAPED_LIST:
                print(raceid + '.csv', 'is already scraped')
                continue
            df = Url_scraping(url, driver)
            # csv保存
            df.to_csv(SAVE_DIR + raceid + ".csv", index=False)
        
        # 検索結果の次のページへ
        try:
            driver.get(nextpage)
        except TimeoutException:
            print("ページの読み込みがタイムアウトしました。")
            break
        except WebDriverException as e: #次のページがない場合
            print(f"WebDriverエラーが発生しました: {e}")
            break

    # 終了
    driver.close()



if __name__ == "__main__": 

    All_cource_scraping() 