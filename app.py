import obspython as obs
import requests
import time
import threading  # threadingを使用して非同期処理を行う

# OBSのテキストソース名
text_source_name = "MirrativUserList"

# 設定可能なパラメータ
live_id = "MPnHqKHQjnFWNwhK55z0fg"
page = 1

# 更新インターバル（秒）
UPDATE_INTERVAL = 20

def update_names():
    try:
        # ログ出力: update_namesが実行されているか確認
        obs.script_log(obs.LOG_INFO, "update_names function called.")
        
        url = f"https://www.mirrativ.com/api/live/online_users?live_id={live_id}&page={page}"
        headers = {
            "User-Agent": "MR_APP/10.97.0/Android/Switch/14"
        }
        res = requests.get(url, headers=headers)
        res.raise_for_status()  # HTTPエラーがあった場合に例外を発生させる
        data = res.json()

        if 'users' not in data:
            raise ValueError("Invalid data format: 'users' key not found")

        users = data.get("users", [])

        # ユーザー情報をテキストとして整形
        text = "\n".join([user["name"] for user in users if "name" in user])
        if not text:
            text = "ユーザーが見つかりませんでした。"

        # テキストソースを更新
        source = obs.obs_get_source_by_name(text_source_name)
        if source is not None:
            settings = obs.obs_data_create()
            obs.obs_data_set_string(settings, "text", text)
            obs.obs_source_update(source, settings)
            obs.obs_data_release(settings)
            obs.script_log(obs.LOG_INFO, f"Text source '{text_source_name}' updated with user names.")
        else:
            raise ValueError(f"Text source '{text_source_name}' not found in OBS")

    except requests.exceptions.RequestException as e:
        obs.script_log(obs.LOG_ERROR, f"Network error: {str(e)}")
        text = f"ネットワークエラーが発生しました: {str(e)}"
        update_text_source(text)
    except ValueError as e:
        obs.script_log(obs.LOG_ERROR, f"Data error: {str(e)}")
        text = f"データエラー: {str(e)}"
        update_text_source(text)
    except Exception as e:
        obs.script_log(obs.LOG_ERROR, f"General error: {str(e)}")
        text = f"エラーが発生しました: {str(e)}"
        update_text_source(text)

def update_text_source(text):
    source = obs.obs_get_source_by_name(text_source_name)
    if source is not None:
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", text)
        obs.obs_source_update(source, settings)
        obs.obs_data_release(settings)
        obs.script_log(obs.LOG_INFO, "Text source updated with error message.")
    else:
        obs.script_log(obs.LOG_ERROR, f"Text source '{text_source_name}' not found in OBS")

# OBSの設定画面からパラメータを取得する関数
def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_text(props, "live_id", "ライブID", 0)  # 0はデフォルトのテキスト入力
    obs.obs_properties_add_int(props, "page", "ページ", 1, 1, 10)
    return props

def script_update(settings):
    global live_id, page
    live_id = obs.obs_data_get_string(settings, "live_id")
    page = obs.obs_data_get_int(settings, "page")
    
    # 設定更新時にログを出力
    obs.script_log(obs.LOG_INFO, f"Settings updated: live_id={live_id}, page={page}")
    
    # 別スレッドで定期的にupdate_names関数を呼び出す
    def start_update_loop():
        while True:
            update_names()
            time.sleep(UPDATE_INTERVAL)  # 10秒ごとに実行

    # 新しいスレッドで更新ループを開始
    update_thread = threading.Thread(target=start_update_loop)
    update_thread.daemon = True  # OBSが終了したときにスレッドも終了するようにする
    update_thread.start()
