import mysql.connector

cnx = None

try:
    cnx = mysql.connector.connect(
        user='root',  # ユーザー名
        password='hmjn9577JunJun91',  # パスワード
        host='localhost'  # ホスト名(IPアドレス）
    )

    if cnx.is_connected:
        print("Connected!")

except Exception as e:
    print(f"Error Occurred: {e}")

finally:
    if cnx is not None and cnx.is_connected():
        cnx.close()