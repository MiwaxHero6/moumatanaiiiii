#watchdog
import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# JSONファイルのパス
NUMBER_PATH = './app/numbers.json'

class Value1ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print('aaaa')
        if event.src_path == NUMBER_PATH:
            self.check_value1_update()

    def check_value1_update(self):
        try:
            with open(NUMBER_PATH, 'r') as file:
                data = json.load(file)
                # value1の値を取得
                value1 = data.get('yobidasi')
                print(f'Yobidasi has been updated to: {value1}')
        except (json.JSONDecodeError, IOError) as e:
            print(f'Error reading JSON file: {e}')

if __name__ == "__main__":
    event_handler = Value1ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=NUMBER_PATH, recursive=False)
    
    print(f'Starting to watch for changes in {NUMBER_PATH}...')
    observer.start()

    try:
        while True:
            # スリープしてイベントを待つ
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
