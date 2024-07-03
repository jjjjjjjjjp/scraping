import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# SQLite データベースに接続
conn = sqlite3.connect('race_results.db')
TIMEDELTA_SEC = 0.5 # 時間間隔の粒度を設定
# 出力先のフォルダを設定
output_folder = 'png'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# クエリを実行してデータを取得する関数
def fetch_data(query, params=()):
    cursor = conn.cursor()
    cursor.execute(query, params)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df

# FinishPositionの範囲を指定してデータを取得する関数
def fetch_data_by_position(position_start, position_end):
    query = """
    SELECT Distance, Course, Direction, Time, Finish_position
    FROM race_results
    WHERE Finish_position BETWEEN ? AND ?
    """
    df = fetch_data(query, (position_start, position_end))

    # Timeを"mm:ss.0"形式から秒数に変換
    df['Time'] = pd.to_datetime(df['Time'], format='%M:%S.%f').dt.time
    df['Time_seconds'] = df['Time'].apply(lambda x: datetime.combine(datetime.min, x) - datetime.min).dt.total_seconds()

    return df

def fetch_data_by_distance(distance_start, distance_end):
    query = """
    SELECT Distance, Course, Direction, Time, Finish_position
    FROM race_results
    WHERE Distance BETWEEN ? AND ?
    """
    df = fetch_data(query, (distance_start, distance_end))

    # Timeを"mm:ss.0"形式から秒数に変換
    df['Time'] = pd.to_datetime(df['Time'], format='%M:%S.%f').dt.time
    df['Time_seconds'] = df['Time'].apply(lambda x: datetime.combine(datetime.min, x) - datetime.min).dt.total_seconds()

    return df

def fetch_data_by_course(course):
    query = """
    SELECT Distance, Course, Direction, Time, Finish_position
    FROM race_results
    WHERE Course = ?
    """
    df = fetch_data(query, (course,))

    # Timeを"mm:ss.0"形式から秒数に変換
    df['Time'] = pd.to_datetime(df['Time'], format='%M:%S.%f').dt.time
    df['Time_seconds'] = df['Time'].apply(lambda x: datetime.combine(datetime.min, x) - datetime.min).dt.total_seconds()

    return df

def fetch_data_by_direction(direction):
    query = """
    SELECT Distance, Course, Direction, Time, Finish_position
    FROM race_results
    WHERE Direction = ?
    """
    df = fetch_data(query, (direction,))

    # Timeを"mm:ss.0"形式から秒数に変換
    df['Time'] = pd.to_datetime(df['Time'], format='%M:%S.%f').dt.time
    df['Time_seconds'] = df['Time'].apply(lambda x: datetime.combine(datetime.min, x) - datetime.min).dt.total_seconds()

    return df

# 各組み合わせごとに分布をプロットする関数
def plot_distribution_by_combinations(position_start, position_end):
    df = fetch_data_by_position(position_start, position_end)

    # Distance、Course、Directionの組み合わせごとに分布をプロット
    combinations = df.groupby(['Distance', 'Course', 'Direction'])
    for (distance, course, direction), data in combinations:
        plot_single_combination(data, distance, course, direction)

# 単一の組み合わせに対して分布をプロットする関数
def plot_single_combination(df, distance, course, direction):
    fig, ax = plt.subplots(figsize=(10, 6))
    timedelta_seconds = TIMEDELTA_SEC  # 時間間隔の粒度を設定

    counts = []
    start_time = df['Time_seconds'].min()
    end_time = df['Time_seconds'].max()

    current_time = start_time
    while current_time <= end_time:
        count = df[(df['Time_seconds'] >= current_time) & 
                   (df['Time_seconds'] < current_time + timedelta_seconds)].shape[0]
        counts.append(count)
        current_time += timedelta_seconds

    time_values = [datetime.min + timedelta(seconds=start_time + i * timedelta_seconds) for i in range(len(counts))]
    time_strings = [time.strftime('%M:%S.%f')[:-3] for time in time_values]  # mm:ss.00 形式に変換

    ax.plot(time_strings, counts)
    ax.set_xlabel('Time')
    ax.set_ylabel('Count')
    ax.set_title(f"Time distribution - Distance {distance}, Course {course}, Direction {direction}")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    # 画像ファイル名の作成と保存
    file_name = f"Timedistribution_{distance}m__{course}_{direction}.png"
    file_path = os.path.join(output_folder, file_name)
    plt.savefig(file_path)
    plt.close()

# メイン処理
if __name__ == "__main__":
    position_start = 1  # 開始Finish_positionを設定
    position_end = 3    # 終了Finish_positionを設定
    plot_distribution_by_combinations(position_start, position_end)

    conn.close()
