from flask import Flask, request
import os
import google.generativeai as genai

app = Flask(__name__)

# 環境変数からAPIキーを取得
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

def load_prompt():
    prompt_path = os.path.join("prompt", "mh_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()

HASHTAGS = """
#モンハンワイルズ
#モンハン
#モンスターハンター
#MHWilds
#モンスターハンターワイルズ
#モンハンワイルズ募集
"""

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    prompt = load_prompt()
    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        result_with_tags = f"{result}\n{HASHTAGS.strip()}"
        print(f"💬 Geminiの応答:\n{result_with_tags}")
        return result_with_tags
    except Exception as e:
        return f"❌ エラー: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
