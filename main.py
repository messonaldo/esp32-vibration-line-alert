from flask import Flask, request
import datetime
import logging
import threading
import time
import requests

app = Flask(__name__)

# Logging 設定
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# LINE Messaging API
LINE_NOTIFY_URL = "https://api.line.me/v2/bot/message/push"
LINE_ACCESS_TOKEN = "GxKQCTE6XpBYDN9Z/WtWQVAR3WEkAwR/5eGIN2MXlfiXohV3BjxTYalySy2HBN7rLmyaTtMj/ONe+FUCZa3etR5aXqroXqGxyQUkPZ+9Kfwj7X/++HrngGIkT7/bWcKRQAionzH0QC/YByoEmW9rDgdB04t89/1O/w1cDnyilFU="

# 推播對象 LINE 使用者 ID
TO_USER_ID = "Ue428e46d6380ba97aaca7b234375bf3c"

# 儲存最後一次接收訊號時間與狀態
last_signal_time = time.time()
last_flag = None

def send_line_message(message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    payload = {
        "to": TO_USER_ID,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }
    response = requests.post(LINE_NOTIFY_URL, headers=headers, json=payload)
    if response.status_code != 200:
        logging.warning(f"LINE message failed: {response.text}")

# 背景監聽線程：超過 60 秒沒收到資料，顯示 Empty 並傳 LINE
def monitor_signal():
    global last_signal_time
    while True:
        time.sleep(60)  # ← 將時間從 10 秒改為 60 秒
        if time.time() - last_signal_time > 60:
            logging.info("Empty")
            send_line_message("Empty")

# 啟動背景監控
threading.Thread(target=monitor_signal, daemon=True).start()

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time, last_flag
    data = request.get_json()
    if not data or 'flag' not in data:
        logging.warning("Missing 'flag' in request.")
        return {"status": "error", "message": "No flag provided"}, 400

    flag = data['flag']
    last_signal_time = time.time()

    if flag == 1:
        logging.info("Motor ON")
        if last_flag != 1:
            send_line_message("Motor ON")
    elif flag == 0:
        logging.info("Motor OFF")
        # 不發 LINE 訊息
    else:
        logging.warning(f"Unknown flag value received: {flag}")

    last_flag = flag
    return {"status": "success"}
