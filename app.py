import asyncio
import csv
import os
from datetime import datetime
from random import randint
from flask import Flask, request, jsonify
from flask_cors import CORS
from twikit import Client, TooManyRequests
from configparser import ConfigParser
from OpenAi_call import OpenAi_call
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load login credentials from environment variables
username = os.getenv("USERNAME")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize Twitter client
client = Client(language='en-US')

BASE_QUERY = "(crypto OR bitcoin OR ethereum OR dogecoin OR shiba OR memecoin OR defi) lang:en"
MINIMUM_TWEETS = 10

async def login():
    """Handles login using cookies or credentials."""
    if not os.path.exists('cookies.json') or os.stat('cookies.json').st_size == 0:
        print(f'{datetime.now()} - Logging in...')
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')

async def get_tweets(tweets, query):
    """Fetches tweets based on the provided query."""
    if tweets is None:
        print(f'{datetime.now()} - Fetching tweets...')
        tweets = await client.search_tweet(query, product='Top')  
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Fetching next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)  
        tweets = await tweets.next()  

    return tweets

async def fetch_tweets(query):
    """Handles fetching tweets and saving them to CSV."""
    await login()
    client.load_cookies('cookies.json')

    tweet_count = 0
    tweets = None
    tweet_list = []

    # Overwrite CSV every time
    with open('crypto_tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets, query)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            await asyncio.sleep(wait_time)
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = {
                "Tweet_count": tweet_count,
                "Username": tweet.user.name,
                "Text": tweet.text.replace("\n", " "),
                "Created_At": tweet.created_at,
                "Retweets": tweet.retweet_count,
                "Likes": tweet.favorite_count
            }
            tweet_list.append(tweet_data)

            # Write to CSV file
            with open('crypto_tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data.values())

        print(f'{datetime.now()} - Collected {tweet_count} tweets')

    return tweet_list  # Return the collected tweets

@app.route('/fetch_tweets', methods=['GET'])
def fetch_tweets_api():
    """API endpoint to fetch tweets with an optional custom query."""
    extra_query = request.args.get('query', '').strip()  # Get optional query parameter
    final_query = f"{BASE_QUERY} {extra_query}" if extra_query else BASE_QUERY

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_tweets(final_query))

    # Run sentiment analysis
    results = OpenAi_call()

    return jsonify({
        "status": "success",
        "message": "Tweet collection and sentiment analysis completed!",
        "tweets": results
    })

@app.route('/', methods=['GET'])
def index():
    """Simple index route."""
    return jsonify({
        "status": "success",
        "message": "Welcome to the Crypto Tweet Analyzer API!"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Azure's PORT or fallback to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

