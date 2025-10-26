#log_user_data.py
import json
import datetime

# ログファイル名
LOG_FILE = 'user_data.json'

def log_user_data(user_id, timestamp):
    data = {
        'user_id': user_id,
        'timestamp': timestamp
    }
    
    try:
        with open(LOG_FILE, 'a') as f:
            json.dump(data, f)
            f.write('\n')
    except IOError as e:
        print(f"Error writing to file: {e}")

user_id = 628495710849719546278
timestamp = 21783647198

log_user_data(user_id, timestamp)
