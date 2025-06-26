from flask import Flask, request
import os
import google.generativeai as genai

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    prompt = "今日の面白い一言をください（140文字以内で）"
    try:
        response = model.generate_content(prompt)
        result = response.text
        print(f"💬 Geminiの応答: {result}")
        return result  # GAS側で受け取れる
    except Exception as e:
        return f"❌ エラー: {e}", 500
