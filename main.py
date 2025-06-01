from flask import Flask, request
import datetime
import logging

# 設定 logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or 'flag' not in data:
        logging.warning("Missing 'flag' in request.")
        return {"status": "error", "message": "No flag provided"}, 400

    flag = data['flag']

    if flag == 1:
        logging.info("Motor ON")
    elif flag == 0:
        logging.info("Motor OFF")
    else:
        logging.warning(f"Unknown flag value received: {flag}")

    return {"status": "success"}
