from flask import Flask, request
import os
import google.generativeai as genai
import tweepy

app = Flask(__name__)

# --- Gemini 設定 ---
API_KEY = os.getenv("GEMINI_API_KEY")
PROMPT = os.getenv("PROMPT_TEXT")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# --- X (旧Twitter) 認証 ---
CONSUMER_KEY = os.getenv("API_KEY")
CONSUMER_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# --- 固定ハッシュタグ ---
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
    if not PROMPT:
        return "❌ PROMPT_TEXT の環境変数が設定されていません。", 500

    try:
        # Gemini で文章生成
        response = model.generate_content(PROMPT)
        result = response.text.strip()
        tweet = f"{result}\n{HASHTAGS.strip()}"

        # X に投稿
        api.update_status(tweet)
        print(f"✅ 投稿成功:\n{tweet}")
        return f"✅ ツイート完了:\n{tweet}"
    except Exception as e:
        print(f"❌ 投稿失敗: {e}")
        return f"❌ エラー: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
