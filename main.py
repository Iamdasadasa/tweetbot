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

# --- X (v2 API) 認証 ---
client = tweepy.Client(
    consumer_key=os.getenv("API_KEY"),
    consumer_secret=os.getenv("API_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

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

        # X (v2) に投稿
        client.create_tweet(text=tweet)
        print(f"✅ 投稿成功:\n{tweet}")
        return f"✅ ツイート完了:\n{tweet}"
    except Exception as e:
        print(f"❌ 投稿失敗: {e}")
        return f"❌ エラー: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
