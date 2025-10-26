import json
import tempfile
import os
import shutil

def update_reservation_in_place(file_path, reservation_number, new_user_id):
    # 一時ファイルを作成
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
    
    updated = False
    try:
        # 元のファイルを読み込み、一時ファイルに書き込む
        with open(file_path, 'r') as file:
            for line in file:
                reservation = json.loads(line.strip())
                
                # 指定された予約番号と一致する場合、ユーザーIDを更新
                if reservation.get('yoyaku') == reservation_number:
                    reservation['user_id'] = new_user_id
                    updated = True
                
                # 更新されたデータを一時ファイルに書き込む
                json.dump(reservation, temp_file)
                temp_file.write('\n')
        
        temp_file.close()
        
        # 元のファイルを一時ファイルで置き換える
        shutil.move(temp_file.name, file_path)
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラーが発生した場合、一時ファイルを削除
        os.unlink(temp_file.name)

# 使用例
file_path = 'user_data2.json'
reservation_number_to_update = 3
new_user_id = '0'

update_reservation_in_place(file_path, reservation_number_to_update, new_user_id)