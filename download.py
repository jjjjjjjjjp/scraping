import os
from urllib.request import *

print("ダウンロード開始")

# HTMLファイル 保存先のディレクトリ
save_dir = os.path.dirname(os.path.abspath(__file__)) + "/html/"

# 存在しなければディレクトリ作成
if not os.path.exists(save_dir): 
    os.mkdir(save_dir)

# htmlをダウンロードするURL
# ここでは千草ウェブのトップページ
download_url = "https://db.netkeiba.com/race/202205020811/"

# 保存先
save_file = save_dir + "/test.html"

# ダウンロード
urlretrieve(download_url, save_file)

print("ダウンロード完了")