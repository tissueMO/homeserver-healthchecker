################################################################
#    自宅サーバーのヘルスチェックを行います。
################################################################
import os
import json
import requests
from requests.exceptions import RequestException

# 各種設定値を取得
SCHEMA = os.getenv("SCHEMA")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT") or ""
TIMEOUT_SEC = int(os.getenv("TIMEOUT_SEC"))
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def lambda_handler(event, context):
    target_url = f"{SCHEMA}://{HOST}{':' if PORT else ''}{PORT}/"
    try:
        response = requests.get(target_url, timeout=TIMEOUT_SEC)
        health_check_result = response.status_code
        if health_check_result == requests.codes.ok:
            return f"OK"
    except RequestException as e:
        # ネットワーク通信エラー、タイムアウト、リダイレクト無限ループ等
        print(e)
        health_check_result = type(e)

    try:
        response = requests.post(
            SLACK_WEBHOOK_URL,
            data=json.dumps({
                "attachments": [
                    {
                        "color": "danger",
                        "title": "ヘルスチェック失敗",
                        "text": f"失敗理由: {health_check_result}\n{target_url}",
                    },
                ],
            }),
            headers={
                "Content-Type": "application/json"
            }
        )
        if response.status_code != requests.codes.ok:
            return f"NG: Slackアラート送出失敗: {response.status_code}"
        else:
            return f"NG: ヘルスチェック失敗: {health_check_result}"
    except RequestException as e:
        # ネットワーク通信エラー、タイムアウト、リダイレクト無限ループ等
        print(e)
        return f"NG: Slackアラート送出失敗: {type(e)}"
