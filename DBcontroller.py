# 生データの整形やDB
import os
import sqlite3
import csv
import Selfmade_functions as Smf

def csv_to_sqlite(csv_file, db_file, table_name):
    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # テーブルを作成するSQL文を定義
    create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- レコードを一意に識別するためのID、自動インクリメント
        RaceID INTEGER, -- レースID
        Race_name TEXT NOT NULL, -- レース名、NULLを許容しない
        Course TEXT NOT NULL, -- レース会場、NULLを許容しない
        Distance INTEGER NOT NULL, -- レースの距離、NULLを許容しない
        Direction TEXT NOT NULL, -- レースの方向、NULLを許容しない
        Surface TEXT NOT NULL, -- 芝 or ダート、NULLを許容しない
        Track_condition TEXT NOT NULL, -- 馬場、NULLを許容しない
        Weather TEXT, -- レース当日の天候、NULLを許容する
        Gate_num INTEGER, -- 馬の枠番号
        Horse_num INTEGER, -- 馬の馬番号
        Horse_name TEXT NOT NULL, -- 馬の名前、NULLを許容しない
        HorseID INTEGER, -- 馬を識別するためのID
        Sex TEXT, -- 馬の性別
        Age INTEGER, -- 馬の年齢
        Horse_weight INTEGER, -- 馬の体重
        Weight_change INTEGER, -- 馬の体重変化
        Assigned_weight INTEGER, -- 斤量
        Finish_position INTEGER, -- 着順
        Jockey TEXT NOT NULL, -- 騎手の名前、NULLを許容しない
        Time TEXT, -- レースのタイム
        Margin TEXT, -- 1着との差距離
        Passing_positions TEXT, -- 通過順位
        Final_3_furlongs TEXT, -- 最終3ハロンのタイム
        Win REAL, -- 単勝オッズ
        Odds REAL, -- 人気
        Trainer TEXT NOT NULL, -- 調教師の名前、NULLを許容しない
        Owner TEXT NOT NULL, -- 馬主の名前、NULLを許容しない
        Prize_money REAL, -- 獲得賞金
        UNIQUE(RaceID, Horse_num) -- 同じレース内で馬番が重複しないことを保証する
        );
        '''
    cursor.execute(create_table_sql)

    # CSVファイルを開いてデータを読み込み、SQLiteに挿入する
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        print("Reading...", csv_file)
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            race_id = row['raceID']
            horse_num = row['馬番']

            # 既存のデータがあるかどうかをチェック
            if Smf.check_existing_data(conn, race_id, horse_num):
                print(f"RaceID: {race_id}, Horse_num: {horse_num} は既に存在するためスキップします。")
                continue
            insert_sql = f"""
            INSERT INTO {table_name} (
                RaceID, 
                Race_name, 
                Course, 
                Distance, 
                Direction,
                Surface, 
                Track_condition, 
                Weather, 
                Gate_num, 
                Horse_num, 
                Horse_name, 
                HorseID, 
                Sex, 
                Age, 
                Horse_weight,
                Weight_change,
                Assigned_weight,
                Finish_position,
                Jockey,
                Time,
                Margin,
                Passing_positions,
                Final_3_furlongs,
                Win,
                Odds,
                Trainer,
                Owner,
                Prize_money
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            # CSVから取得したデータをタプルに変換して挿入
            values = (
                row['raceID'], 
                row['race_name'],
                row['cource'], 
                row['distance'], 
                row['around'],
                row['groung'], 
                row['groung_state'], 
                row['weather'], 
                row['枠番'],
                row['馬番'],
                row['馬名'],
                row['houceID'], 
                row['sex'],
                row['age'], 
                row['hource_weight'], 
                row['weight_diff'],  
                row['斤量'],
                row['着順'],
                row['騎手'],
                row['タイム'], 
                row['着差'], 
                row['通過'], 
                row['上り'],
                row['単勝'], 
                row['人気'], 
                row['調教師'], 
                row['馬主'], 
                row['賞金(万円)']
            )
            try:
                cursor.execute(insert_sql, values)
            except sqlite3.Error as e:
                print(f"SQLite error occurred: {e}")
                #トランザクションをロールバックする
                conn.rollback()
            except Exception as e:
                print(f"An error occurred: {e}")

    # 変更をコミットしてデータベースを保存し、接続を閉じる
    conn.commit()
    conn.close()
    print("DBinput Conpleted", csv_file)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_folder = os.path.join(script_dir, 'csv')
    db_file = 'race_results.db'
    table_name = 'race_results'
    for csv_file in os.listdir(csv_folder): #すべてのcsvに対して
        if csv_file.endswith('.csv'):
            csv_path = os.path.join(csv_folder, csv_file)
                        
            with sqlite3.connect(db_file) as conn:
                try:
                    csv_reader = csv.DictReader(open(csv_path, 'r', newline='', encoding='utf-8'))
                except FileNotFoundError:
                    print(f"エラー: ファイル '{csv_path}' が見つかりません。")
                except PermissionError:
                    print(f"エラー: ファイル '{csv_path}' へのアクセス権がありません。")
                except csv.Error as e:
                    print(f"エラー: CSVファイルの読み込み中にエラーが発生しました。詳細: {e}")
                except Exception as e:
                    print(f"予期しないエラーが発生しました: {e}")
                try:
                    for row in csv_reader:
                        race_id = row['raceID']
                        horse_num = row['馬番']
                        if Smf.check_existing_data(conn, race_id, horse_num): # ファイルごとに処理をスキップするかどうかを判定
                            print(f"RaceID: {race_id}, Horse_num: {horse_num} は既に存在するため、ファイルの処理をスキップします。")
                            break
                        else:
                            csv_to_sqlite(csv_path, db_file, table_name) #db_fileにcsvデータ投入
                except UnicodeDecodeError as e:
                    print(f"エラー: ファイル '{csv_path}' の読み込み中にエンコードエラーが発生しました。詳細: {e}")

