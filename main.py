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
TELEGRAM_BOT_TOKEN = "7614581082:AAHt4l72rO5G-dJXsBYPje13c0aviLBCl5w"
TELEGRAM_CHAT_ID = "7040024260"  # Telegram User ID

# 儲存最後一次接收訊號時間與狀態
last_signal_time = time.time()
last_flag = None
empty_sent = False  # 確保 Empty 僅發送一次

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

# 背景監聽線程：超過 300 秒沒收到資料，顯示 Empty 並傳 Telegram 訊息
def monitor_signal():
    global last_signal_time, empty_sent
    while True:
        time.sleep(5)
        if time.time() - last_signal_time > 300 and not empty_sent:
            logging.info("Empty")
            send_telegram_message("Empty")
            empty_sent = True  # 防止重複發送

# 啟動背景監控
threading.Thread(target=monitor_signal, daemon=True).start()

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time, last_flag, empty_sent
    data = request.get_json()
    if not data or 'flag' not in data or 'az' not in data:
        logging.warning("Missing 'flag' or 'az' in request.")
        return {"status": "error", "message": "Missing flag or az"}, 400

    flag = data['flag']
    az = data['az']
    last_signal_time = time.time()
    empty_sent = False  # 有資料就重設 Empty 狀態

    if flag == 1:
        log_msg = f"Motor ON, az = {az}"
        telegram_msg = f"Motor ON"
        logging.info(log_msg)
        if last_flag != 1:
            send_telegram_message(telegram_msg)
    elif flag == 0:
        log_msg = f"Motor OFF, az = {az}"
        logging.info(log_msg)
        # flag = 0 不發送 Telegram 訊息
    else:
        logging.warning(f"Unknown flag value received: {flag}")

    last_flag = flag
    return {"status": "success"}

@app.route("/ping", methods=["GET"])
def ping():
    logging.info("Ping received.")
    return "pong", 200
