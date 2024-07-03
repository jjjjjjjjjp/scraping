import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# SQLiteデータベースへの接続とカーソルの取得
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Finish_positionの範囲を指定して、各分布をプロットする関数
def plot_distribution_by_category(finish_positions):
    plot_by_distance(finish_positions)
    plot_by_course(finish_positions)
    plot_by_direction(finish_positions)

# Distance毎の分布を取得
def plot_by_distance(finish_positions):
    query = f"""
    SELECT Distance, Finish_position, COUNT(*) AS Count
    FROM races
    WHERE Finish_position BETWEEN {finish_positions[0]} AND {finish_positions[1]}
    GROUP BY Distance, Finish_position
    ORDER BY Distance, Finish_position
    """
    df = pd.read_sql_query(query, conn)
    plot_distribution(df, "Distance", finish_positions)

# Course毎の分布を取得
def plot_by_course(finish_positions):
    query = f"""
    SELECT Course, Finish_position, COUNT(*) AS Count
    FROM races
    WHERE Finish_position BETWEEN {finish_positions[0]} AND {finish_positions[1]}
    GROUP BY Course, Finish_position
    ORDER BY Course, Finish_position
    """
    df = pd.read_sql_query(query, conn)
    plot_distribution(df, "Course", finish_positions)

# Direction毎の分布を取得
def plot_by_direction(finish_positions):
    query = f"""
    SELECT Direction, Finish_position, COUNT(*) AS Count
    FROM races
    WHERE Finish_position BETWEEN {finish_positions[0]} AND {finish_positions[1]}
    GROUP BY Direction, Finish_position
    ORDER BY Direction, Finish_position
    """
    df = pd.read_sql_query(query, conn)
    plot_distribution(df, "Direction", finish_positions)

# データフレームを受け取り、指定したカラムでグラフをプロットする関数
def plot_distribution(df, category, finish_positions):
    categories = df[category].unique()
    positions = range(finish_positions[0], finish_positions[1] + 1)

    fig, ax = plt.subplots(len(categories), figsize=(10, len(categories) * 5))
    for i, cat in enumerate(categories):
        data = df[df[category] == cat]
        ax[i].bar(data['Finish_position'], data['Count'], color='blue')
        ax[i].set_title(f"{category}: {cat}")
        ax[i].set_xlabel('Finish Position')
        ax[i].set_ylabel('Count')
        ax[i].set_xticks(positions)
        ax[i].set_xticklabels(positions)

    plt.tight_layout()
    plt.show()

# メイン処理
if __name__ == "__main__":
    # Finish_positionの範囲を指定
    finish_positions_1_to_3 = (1, 3)
    finish_positions_1_to_5 = (1, 5)

    # 分布をプロット
    print("Plotting distribution for Finish Positions 1 to 3")
    plot_distribution_by_category(finish_positions_1_to_3)

    print("Plotting distribution for Finish Positions 1 to 5")
    plot_distribution_by_category(finish_positions_1_to_5)

# 接続を閉じる
conn.close()