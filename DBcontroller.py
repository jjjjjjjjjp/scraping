# 生データの整形やDB

import csv
import sqlite3

def csv_to_sqlite(csv_file, db_file, table_name):
    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # テーブルを作成するSQL文を定義（例：カラム名は適宜変更してください）
    create_table_sql = f'''
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        column1 TEXT,
        column2 TEXT,
        column3 INTEGER
        -- ここにカラムの定義を追加
    );
    '''
    cursor.execute(create_table_sql)

    # CSVファイルを開いてデータを読み込み、SQLiteに挿入する
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # ヘッダー行をスキップする場合

        for row in csv_reader:
            # データを挿入するSQL文を定義（例：カラム数と値は適宜変更してください）
            insert_sql = f'''
            INSERT INTO {table_name} (column1, column2, column3)
            VALUES (?, ?, ?);
            '''
            cursor.execute(insert_sql, row)

    # 変更をコミットしてデータベースを保存し、接続を閉じる
    conn.commit()
    conn.close()

# 使用例
csv_file = 'data.csv'  # 変換したいCSVファイルのパス
db_file = 'data.db'    # 保存先のSQLiteデータベースファイル名
table_name = 'my_table'  # 作成するテーブル名

# CSVファイルをSQLiteデータベースに変換する
csv_to_sqlite(csv_file, db_file, table_name)