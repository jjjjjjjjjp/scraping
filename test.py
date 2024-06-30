from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# WebDriverを設定して起動
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # JavaScriptを実行して、カスタムダイアログを生成する例
    js_script = """
    window.onload = function() {
    // ボタンがクリックされたらアラートを表示
    document.getElementById("myButton").onclick = function() {
        alert("ボタンが押されました！");
    };

    // アラートが閉じられるまで再度アラートを表示
    function showRepeatedAlert() {
        alert("ボタンを押してください！");
        setTimeout(showRepeatedAlert, 1000); // 1秒ごとに再度表示
    }
    showRepeatedAlert(); // 最初の表示を開始
    };
    """
    driver.execute_script(js_script)

    # アラートが表示されるまで少し待つ
    driver.switch_to.alert.accept()

except Exception as e:
    print(f"エラーが発生しました: {e}")

finally:
    # ブラウザを閉じる
    driver.quit()