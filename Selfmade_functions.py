#かゆいところに手が届くちょっとした関数たち
import re
import os
import sqlite3

def Print_filepath():
    # 現在実行しているPythonファイルのパスを取得
    current_file_path = os.path.abspath(__file__)

    # ファイルのパスを出力
    print("現在実行中のファイルのパス:", current_file_path)

    os.path.dirname(__file__)


def check_raceid_exists(db_file, race_id):
    """
    指定されたRaceIDがデータベース内に存在するかをチェックする関数。
    
    Parameters:
    - db_file (str): SQLiteデータベースファイルのパス
    - race_id (int): 存在を確認するRaceID
    
    Returns:
    - bool: RaceIDが存在する場合はTrue、存在しない場合はFalse
    """
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # race_resultsテーブルから指定されたRaceIDのレコード数をカウントする
    cursor.execute("SELECT COUNT(*) FROM race_results WHERE RaceID = ?", (race_id,))
    count = cursor.fetchone()[0]
    
    conn.close()
    
    # カウントが1以上ならRaceIDが存在する、それ以外は存在しないと判断
    return count > 0

def check_existing_data(conn, race_id, horse_num):
    """
    データベース内に指定されたレースIDと馬番が既に存在するかをチェックする関数。
    """
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM race_results WHERE RaceID = ? AND Horse_num = ?", (race_id, horse_num))
    count = cursor.fetchone()[0]
    return count > 0

if __name__ == "__main__": 
    Print_filepath()
    input_string = "446(-2)"

    result = split_string(input_string)
    print(result)