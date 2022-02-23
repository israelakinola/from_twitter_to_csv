
from flask import Flask, request, render_template, send_file
import tweepy
import csv


app = Flask(__name__)

### input your credentials here
bearer_token = ''

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form['hashtag'] != '' :
        try:
            fetch(request.form['hashtag'], int(request.form['qty']))
        except:
            pass
        finally:
            return render_template("index.html", hashtag = request.form['hashtag'], fetched = True)
    return render_template("index.html")


def fetch(hashtag, qty):
    auth = tweepy.OAuth2BearerHandler(bearer_auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Open/Create a file to append dataß
    csvFile = open('tweets.csv', 'w')

    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['Created at', 'Username', 'Tweets', 'Retweet Count' 'Likes'])
    for tweet in tweepy.Cursor(api.search_tweets,q=hashtag,
                            lang="en").items(qty):
                            csvWriter.writerow([tweet.created_at, tweet.user.screen_name, tweet.text.encode('utf-8'), tweet.retweet_count, tweet.favorite_count])

@app.route('/download', methods=['GET', 'POST'])
def download():    
    path = "/Users/Kelv_leo/Desktop/fetchtocsv/tweets.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()