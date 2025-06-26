from flask import Flask
import tweepy
import os

app = Flask(__name__)

@app.route("/")
def post_tweet():
    consumer_key = os.getenv("API_KEY")
    consumer_secret = os.getenv("API_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    tweet_text = "今日もがんばろう！ #モンハン #ねむねむ"

    try:
        api.update_status(tweet_text)
        return "✅ ツイート成功！"
    except Exception as e:
        return f"❌ ツイート失敗: {str(e)}"

if __name__ == "__main__":
    app.run()
