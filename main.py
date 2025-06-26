from flask import Flask, request
import os
import google.generativeai as genai

app = Flask(__name__)

# 環境変数からAPIキーを取得
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    prompt = """
【要件】
・出力は日本語のみで書いてください。外国語（英語・ロシア語など）は一切使わないでください。
・文字数は80〜100文字の間にしてください。
・出力は「X（旧Twitter）」のツイートに使います。
・改行は不要です。絵文字は使用OKです。
・以下の雰囲気に合う、優しいサークル勧誘文をお願いします。

【参考文1】
「一緒にやる」って言葉の中には、黙ってても大丈夫、っていう意味も入ってる気がしてて。ねむねむは、そんな場所…

【参考文2】
このサークル、話すのが好きな人も、黙って遊ぶのが好きな人もいて。どっちも歓迎されてるのがいいなって。

【参考文3】
はじめましても大歓迎！優しい人たちと、のんびり楽しく狩りしませんか？🌿

【出力例（形式）】
初心者さんも大歓迎！やさしい雰囲気で、のんびり狩りを楽しみませんか？🌸
"""

    try:
        response = model.generate_content(prompt)
        result = response.text.strip()
        print(f"💬 Geminiの応答: {result}")
        return result  # GAS側で受け取れる
    except Exception as e:
        return f"❌ エラー: {e}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
