from pymongo import MongoClient
from pymongo.server_api import ServerApi
from textblob import TextBlob
import pandas as pd

# Setup MongoDB connection using environment variable for the URI
uri = "mongodb+srv://plin11:2968peter@cluster0.jwnt1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["test"]  # Accessing the 'test' database
    tweets_collection = db["database"]  # Accessing the 'database' collection
    print("Connected to MongoDB, accessing collection.")

    # Fetch tweets data with projection to limit data transfer
    tweets_data = tweets_collection.find({}, {
        'tweet': 1,
        'likes': 1,
        'retweet_count': 1,
        'state_code': 1
    }).limit(5000)

    # Prepare data for analysis
    data = [{
        'tweet': tweet.get('tweet', ''),
        'likes': tweet.get('likes', 0),
        'retweets': tweet.get('retweet_count', 0),
        'state_code': tweet.get('state_code', 'Unknown')
    } for tweet in tweets_data]
    print(f"Retrieved {len(data)} documents.")

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(data)
    print("Data loaded into DataFrame.")

    # Analyze sentiment of each tweet
    df['sentiment'] = df['tweet'].apply(lambda x: TextBlob(x).sentiment.polarity)
    print("Sentiment analysis completed.")

    # Classify sentiment
    df['sentiment_category'] = pd.cut(df['sentiment'], bins=[-1, -0.01, 0.01, 1], labels=['negative', 'neutral', 'positive'])
    print("Sentiment categorized.")

    # Group by state and sentiment category
    summary = df.groupby(['state_code', 'sentiment_category']).agg({
        'likes': 'mean',
        'retweets': 'mean',
        'sentiment': 'count'
    }).rename(columns={'sentiment': 'count'})

    print(summary)
except Exception as e:
    print(f"An error occurred: {e}")
