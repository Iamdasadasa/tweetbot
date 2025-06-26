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
・下記について答えのみで返してください(はい。やわかりました。など会話をする必要はありません)
・Xのツイート用です　必ず80〜100文字程度にしてください

あなたへの要望です
「モンスターハンターワイルズのサークルアカウントに呟く文言を80文字までで考えてください。

優しい空気／初心者も安心感出すタイプのものだったり、サークル勧誘として明るいものなどでよろしくお願いします。
絵文字なども入れて構いません。」

また、これは繰り返し行われる要望です。
あなたのメモリに過去の会話が残っている場合はなるべくでいいので被らないような内容が望ましいです。

参考1
「一緒にやる」って言葉の中には、
黙ってても大丈夫、っていう意味も入ってる気がしてて。
ねむねむは、そんな場所…

参考2
このサークル、話すのが好きな人も、黙って遊ぶのが好きな人もいて。
どっちも、ちゃんと歓迎されてる感じがあるの、いいよなって。

参考3
はじめましても大歓迎！優しい人たちと、のんびり楽しく狩りしませんか？🌿
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
