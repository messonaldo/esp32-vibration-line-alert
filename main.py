from flask import Flask, request
import datetime
import logging
import threading
import time

app = Flask(__name__)

# 設定 logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# 紀錄上次收到訊號的時間
last_signal_time = time.time()

# 背景檢查線程
def monitor_signal():
    global last_signal_time
    while True:
        time.sleep(10)
        if time.time() - last_signal_time > 10:
            logging.info("Empty")

# 啟動背景監測執行緒
threading.Thread(target=monitor_signal, daemon=True).start()

@app.route("/webhook", methods=["POST"])
def webhook():
    global last_signal_time
    data = request.get_json()
    if not data or 'flag' not in data:
        logging.warning("Missing 'flag' in request.")
        return {"status": "error", "message": "No flag provided"}, 400

    flag = data['flag']
    last_signal_time = time.time()  # 更新收到訊號的時間

    if flag == 1:
        logging.info("Motor ON")
    elif flag == 0:
        logging.info("Motor OFF")
    else:
        logging.warning(f"Unknown flag value received: {flag}")

    return {"status": "success"}
