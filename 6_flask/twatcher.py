from flask import Flask, render_template
from tweet_store import TweetStore

app = Flask(__name__)
store = TweetStore()

@app.route('/')
def index():
    tweets = store.tweets()
    return render_template('index.html', tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
