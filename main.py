from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ✅ LINE Notify 權杖（請務必保密）
LINE_TOKEN = "GxKQCTE6XpBYDN9Z/WtWQVAR3WEkAwR/5eGIN2MXlfiXohV3BjxTYalySy2HBN7rLmyaTtMj/ONe+FUCZa3etR5aXqroXqGxyQUkPZ+9Kfwj7X/++HrngGIkT7/bWcKRQAionzH0QC/YByoEmW9rDgdB04t89/1O/w1cDnyilFU="

# ✅ 根目錄 - 確保網址打開不是 404
@app.route("/", methods=["GET"])
def home():
    return "✅ LINE Notify API is running. Use POST /notify"

# ✅ 通知路由 - ESP32 發送資料用
@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    freq = data.get("freq", 0)
    amp = data.get("amp", 0)

    print("📡 接收到資料：", data)

    # ✅ 符合條件就發送通知
    if freq == 100 and amp >= 5:
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "message": "✅ ON 通知：主頻為 100Hz，振幅大於等於 5"
        }
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
        print("📬 發送 LINE Notify 結果：", r.status_code)
        return "Sent" if r.status_code == 200 else "Failed", r.status_code

    return "No action needed", 200
