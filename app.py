
from flask import Flask, redirect, request, render_template, send_file,flash, url_for
import tweepy
import csv


app = Flask(__name__)
app.secret_key = "auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!"
### input your credentials here
bearer_token = "AAAAAAAAAAAAAAAAAAAAAO2jZAEAAAAADsaC86PsPGWfiFLidgGsyl55kQw%3Dw62k3WJy7yVb1LPqUTkwGlXy4oFGw5JRLFKf1WZGNt6vVs6AvJ"

@app.route("/", methods=['POST', 'GET'])
def index():
    """
        This function return the Index HTML Template and its form handling
    Return
    ______
        HTML Template

    """
    if request.method == 'POST' and request.form['keyword'] != '':
        qty = request.form['qty']
        try:
            qty = int(qty)
        except ValueError:
            flash("Qty is not a valid number", "error")
            return redirect(url_for('index'))
        if (qty > 0 ):
            try:
                fetch(request.form['keyword'], qty)
            except:
                flash("Could not fetch tweets", "error")
        else:
            flash("Qty must be greater than Zero", "error")
            return redirect(url_for('index'))
        
        return render_template("index.html", keyword= request.form['keyword'], fetched = True)
    return render_template("index.html")


def fetch(keyword, qty):
    """
        This function fetch the tweets and write it to a CSV file.

    Arguments
    _________
        keyword <String> : Users keyword that need to be fetched
        qty <Int> : User inputed amount of tweets that need to be fetched
        


    """
    auth = tweepy.OAuth2BearerHandler(bearer_token)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Open/Create a file to append dataß
    csvFile = open('tweets.csv', 'w')

    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['Created at', 'Username', 'Tweets', 'Retweet Count' 'Likes'])
    for tweet in tweepy.Cursor(api.search_tweets,q=keyword,
                            lang="en").items(qty):
                            csvWriter.writerow([tweet.created_at, tweet.user.screen_name, tweet.text.encode('utf-8'), tweet.retweet_count, tweet.favorite_count])

@app.route('/download', methods=['GET', 'POST'])
def download():    
    """
        This function handle the CSV File download

    Return
    _________
        File Path <String>
    """
    path = "/Users/Kelv_leo/Desktop/fetchtocsv/tweets.csv"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    """
        This function run the file if its the main file
    """
    app.debug = True
    app.run()