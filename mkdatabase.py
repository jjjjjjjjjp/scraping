import mysql.connector
import MySQLdb
import re
import csv
import pandas as pd
import os
import glob
import numpy as np

from pathlib import Path

from pymysql import NULL

def make_query():
    query = ''

cnx = None

cnx = MySQLdb.connect(
db = "test",
user = "root",
passwd = '',
host='localhost',
)

path = os.path.dirname(__file__) + '/csv/*csv'
csv_files = glob.glob(path)

df = pd.DataFrame()

for i in csv_files:
    tmp = pd.read_csv(i)
    df = pd.concat([df, tmp])

df = df.rename(columns={
    '着順':'posision',
    '枠番': 'bracket',
    '馬番':'number', 
    '馬名':'hource_name',
    '斤量':'weight',
    '騎手':'jockey',
    'タイム':'time',
    '着差':'margin',
    '人気':'favorite',
    '通過':'posision',
    '上り':'3_furlong',
    '単勝':'Odds',
    '調教師':'breeder',
    '馬主':'owner',
    '賞金(万円)':'stakes_money',
    '馬体重':'hource_weight'
    })

try:
    df = df.rename(columns={'houceID':'hourceID'})
except:
    None

df = df.replace({np.nan: None})

# print(df.columns.to_list())

# for val in df.values:
#     for cell in val:
#         # print(cell)

cursor = cnx.cursor()

# テーブル削除
# query = 'DROP TABLE IF EXISTS race_result'
# cursor.execute(query)

# テーブルの作成
query = 'CREATE TABLE IF NOT EXISTS race_result ('
for i, col in enumerate(df.columns.to_list()):
    query += col + ' VARCHAR(50) NULL ,' 

query = query + ' unique hource_race_ID (hourceID, raceID) )'

# print(query)

cursor.execute(query)

# レース結果のINSERT
for val in df.values:
    query = "INSERT IGNORE INTO race_result ("
    for i, col in enumerate(df.columns.to_list()):
        query += col +','
    query = query[:-1] + ' ) VALUES ( '
    for i, cell in enumerate(val):
        query += "%s,"
    query = query[:-1] + ")"

print(query)


cursor.executemany(query, df.values.tolist())
cnx.commit()

# テーブルの作成
# cursor.execute("""CREATE TABLE race_result(
#     id INT(11) NOT NULL, 
#     name VARCHAR(30) NOT NULL COLLATE utf8mb4_unicode_ci, 
#     age INT(3) NOT NULL,
#     PRIMARY KEY (id)
#     )""")

# データの追加
# cursor.execute("""INSERT INTO name_age_list (name, age)
#     VALUES ('test1', '1'),
#     ('test2', '2'),
#     ('test3', '3')
#     """)

# 一覧の表示
cursor.execute("SELECT * FROM race_result")

for row in cursor:
    print(row)


# 保存を実行
cnx.commit()

# 接続を閉じる
cnx.close()

