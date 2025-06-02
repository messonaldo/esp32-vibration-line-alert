from flask import Flask, request
import time
import threading
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "你的_Telegram_Bot_Token"
TELEGRAM_USER_ID = "你的_Telegram_用戶ID"
CHECK_INTERVAL = 600  # 600 秒內沒收到訊號就傳 Empty

last_signal_time = time.time()
lock = threading.Lock()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_USER_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        print("Telegram sent:", response.json())
    except Exception as e:
        print("Telegram failed:", str(e))

def signal_monitor():
    global last_signal_time
    while True:
        time.sleep(10)
        with lock:
            elapsed = time.time() - last_signal_time
        if elapsed > CHECK_INTERVAL:
            send_telegram_message("⚠️ Empty：300 秒內未接收到任何 flag 訊號。")
            with lock:
                last_signal_time = time.time()  # reset 防止重複發送

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time
    data = request.json
    print("Received:", data)
    if "flag" in data:
        with lock:
            last_signal_time = time.time()
    return "OK", 200

@app.route("/ping", methods=["GET"])
def ping():
    return "Pong!", 200

# 啟動背景監控執行緒
threading.Thread(target=signal_monitor, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
