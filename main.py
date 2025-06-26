from flask import Flask
import os
import google.generativeai as genai

app = Flask(__name__)

# 環境変数からAPIキー取得
API_KEY = os.getenv("GEMINI_API_KEY")

# Geminiの初期化
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

@app.route("/")
def generate_response():
    prompt = "今日の面白い一言をください（140文字以内で）"
    try:
        response = model.generate_content(prompt)
        result = response.text
        print(f"💬 Geminiの応答: {result}")
        return f"✅ Gemini応答を取得: {result}"
    except Exception as e:
        return f"❌ エラー: {e}"

if __name__ == "__main__":
    app.run()
