from flask import Flask, request
import datetime
import logging
import threading
import time
import requests

app = Flask(__name__)

# Logging 設定
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Telegram Bot 資訊
TELEGRAM_BOT_TOKEN = "7837165005:AAEI7SRhFPEsAX4dERqduwSQZwaE-vVaFVw"
TELEGRAM_CHAT_ID = "1989734396"  # 你的 Telegram User ID

# 儲存最後一次接收訊號時間與狀態
last_signal_time = time.time()
last_flag = None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            logging.warning(f"Telegram message failed: {response.text}")
    except Exception as e:
        logging.warning(f"Telegram message exception: {e}")

# 背景監聽線程：超過 60 秒沒收到資料，顯示 Empty 並傳 Telegram 訊息
def monitor_signal():
    global last_signal_time
    while True:
        time.sleep(60)
        if time.time() - last_signal_time > 60:
            logging.info("Empty")
            send_telegram_message("Empty")

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
            send_telegram_message("Motor ON")
    elif flag == 0:
        logging.info("Motor OFF")
        # flag=0 時不發送訊息
    else:
        logging.warning(f"Unknown flag value received: {flag}")

    last_flag = flag
    return {"status": "success"}
