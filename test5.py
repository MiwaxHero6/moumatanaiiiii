#datetime.py
from datetime import datetime, timezone, timedelta

def convert_timestamp_to_japan_time(timestamp):
    # タイムスタンプをUTCのdatetimeオブジェクトに変換
    dt_utc = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    # 日本時間のタイムゾーンオフセットを設定（日本はUTC+9時間）
    japan_offset = timezone(timedelta(hours=9))
    
    # 日本時間に変換
    dt_japan = dt_utc.astimezone(japan_offset)
    
    return dt_japan

# 例: タイムスタンプを指定（例: 1609459200は2021年1月1日の00:00:00 UTC）
timestamp = 1609459200
japan_time = convert_timestamp_to_japan_time(timestamp)
print(japan_time)
