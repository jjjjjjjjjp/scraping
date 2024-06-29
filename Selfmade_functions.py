#かゆいところに手が届くちょっとした関数たち
import re
import os

def Print_filepath():
    # 現在実行しているPythonファイルのパスを取得
    current_file_path = os.path.abspath(__file__)

    # ファイルのパスを出力
    print("現在実行中のファイルのパス:", current_file_path)

    os.path.dirname(__file__)

def split_string(input_string):
    # 正規表現パターンで数値と括弧内の数値をキャプチャ
    pattern = r'(\d+)\((-?\d+)\)'
    
    # 正規表現を使ってマッチを探す
    match = re.match(pattern, input_string)
    
    if match:
        # キャプチャされたグループを取得
        number1 = int(match.group(1))
        number2 = int(match.group(2))
        return number1, number2
    else:
        raise ValueError("入力文字列がフォーマットに一致しません")
    
if __name__ == "__main__": 
    Print_filepath()
    input_string = "446(-2)"

    result = split_string(input_string)
    print(result)