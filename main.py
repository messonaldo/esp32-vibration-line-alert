from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 設定你的 LINE 權杖與使用者 ID（請將下方值換成你自己的）
LINE_TOKEN = "GxKQCTE6XpBYDN9Z/WtWQVAR3WEkAwR/5eGIN2MXlfiXohV3BjxTYalySy2HBN7rLmyaTtMj/ONe+FUCZa3etR5aXqroXqGxyQUkPZ+9Kfwj7X/++HrngGIkT7/bWcKRQAionzH0QC/YByoEmW9rDgdB04t89/1O/w1cDnyilFU="
USER_ID = "Ue428e46d6380ba97aaca7b234375bf3c"

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    freq = data.get("freq", 0)
    amp = data.get("amp", 0)

    # 偵測主頻 = 100 且振幅 >= 5 就發送 LINE 通知
    if freq == 100 and amp >= 5:
        headers = {
            "Authorization": "Bearer 你的長效 Channel access token",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "message": "ON (Frequency = 100Hz, Amplitude ≥ 5)"
        }
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
        return "Sent" if r.status_code == 200 else "Failed", r.status_code

    return "No action", 200

app.run(host="0.0.0.0", port=5000)