
from flask import Flask, request, render_template, send_file
import tweepy
import csv


app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST' and request.form['hashtag'] != '' :
        try:
            fetch(request.form['hashtag'])
        except:
            pass
        finally:
            return render_template("index.html", hashtag = request.form['hashtag'], fetched = True)
    return render_template("index.html")


def fetch(hashtag):
    # input your credentials here
    hashtag = hashtag
    auth = tweepy.OAuth2BearerHandler("AAAAAAAAAAAAAAAAAAAAAO2jZAEAAAAAeHKHp0U%2FLLbThLbR94yZREvpJ54%3Dc2S9jqbpzhQYhrGHa9w8cT8Td7YHMtlsVUmr8C1Tf4vXnoqEBD")
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Open/Create a file to append data
    csvFile = open('tweets.csv', 'a')

    #Use csv Writer
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search_tweets,q=hashtag,
                            lang="en").items(20):
                            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])

@app.route('/download', methods=['GET', 'POST'])
def download():    
    path = "/Users/Kelv_leo/Desktop/fetchtocsv/tweets.csv"
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.debug = True
    app.run()