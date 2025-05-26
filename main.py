from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# LINE Notify 權杖
LINE_TOKEN = "GxKQCTE6XpBYDN9Z/WtWQVAR3WEkAwR/5eGIN2MXlfiXohV3BjxTYalySy2HBN7rLmyaTtMj/ONe+FUCZa3etR5aXqroXqGxyQUkPZ+9Kfwj7X/++HrngGIkT7/bWcKRQAionzH0QC/YByoEmW9rDgdB04t89/1O/w1cDnyilFU="

@app.route("/notify", methods=["POST"])
def notify():
    data = request.get_json()
    freq = data.get("freq", 0)
    amp = data.get("amp", 0)

    if freq == 100 and amp >= 5:
        headers = {
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {
            "message": "ON (Frequency = 100Hz, Amplitude ≥ 5)"
        }
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, data=payload)
        return "Sent" if r.status_code == 200 else "Failed", r.status_code

    return "No action", 200