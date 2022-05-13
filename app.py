from flask import Flask, redirect, request, render_template, send_file, flash, url_for
import tweepy
import csv
from os import getcwd


app = Flask(__name__)

app.secret_key = "auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!"

# Input your Twitter Bearer Token here
bearer_token = ""

download_file_path = f"{getcwd()}/downloads"


@app.route("/", methods=["POST", "GET"])
def index():
    """
        This function return the Index HTML Template and its form handling
    Return
    ______
        HTML Template

    """
    if request.method == "POST" and request.form["keyword"] != "":
        # Fetch tweets
        if validate_keyword:
            tweets = fetch(request.form["keyword"], validate_qty(request.form["qty"]))
            # save to CSV
            save_to_csv(tweets, request.form["keyword"])
            return render_template(
                "index.html", keyword=request.form["keyword"], fetched=True
            )
    return render_template("index.html")


def validate_qty(qty):
    """
        This function validate the Quantity of tweets a user inputed
    Arguments
    _________
    qty: <int> Number of tweets users want to fetch.

    Return
    ______
         qty: <int> Number of tweets users want to fetch. Default is 10
    """
    converted = False
    try:
        qty = int(qty)
    except ValueError:
        pass
    else:
        converted = True

    # Check if qty was converted to
    if converted:
        # check if int is greater than zero
        if qty > 0:
            return qty
    # Set qty to a default 0f 10 and return qty
    qty = 10
    return qty


def validate_keyword(keyword):
    """
        This function validate the Keyword of tweets a user inputed
    Arguments
    _________
    keyword: <int> Number of tweets users want to fetch.

    Return
    ______
         Bool: <bool> True represent keyword was validated, False represent not validated
    """
    # check if keyword length is greater than zero
    if (len(keyword)) <= 0:
        return False
    return True


def fetch(keyword, qty):
    """
        This function fetch the tweets and returns the tweets object

    Arguments
    _________
        keyword <String> : Users keyword that need to be fetched
        qty <Int> : User inputed amount of tweets that need to be fetched

    Return
    ______
        Tweets Objects

    """
    auth = tweepy.OAuth2BearerHandler(bearer_token)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return tweepy.Cursor(api.search_tweets, q=keyword, lang="en").items(qty)


def save_to_csv(tweets, keyowrd_as_file_name):
    """
        This function loop through tweets objects and write them to a CSV file

    Arguments
    _________
        tweets <List> : Tweets objects

    """
    cwd = getcwd()
    # Open/Create a file to append data
    csvFile = open(f"{download_file_path}/{keyowrd_as_file_name}.csv", "w")
    # Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["Created at", "Username", "Tweets", "Retweet Count", "Likes"])
    for tweet in tweets:
        csvWriter.writerow(
            [
                tweet.created_at,
                tweet.user.screen_name,
                tweet.text.encode("utf-8"),
                tweet.retweet_count,
                tweet.favorite_count,
            ]
        )


@app.route("/downloads/<keyowrd_as_file_name>", methods=["GET", "POST"])
def download(keyowrd_as_file_name):
    """
        This function handle the CSV File download

    Return
    _________
        File Path <String>
    """
    path = f"{download_file_path}/{keyowrd_as_file_name}.csv"
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    """
    This function run the file if its the main file
    """
    app.debug = True
    app.run()
