import pandas as pd
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from prettytable import PrettyTable
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

us_state_codes = {'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 
                  'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 
                  'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
                  'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 
                  'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'}
# Ensure necessary NLTK resources are downloaded
nltk.download('vader_lexicon')
nltk.download('punkt')

# Initialize the VADER sentiment analyzer and access the lexicon directly
sia = SentimentIntensityAnalyzer()
vader_lexicon = sia.lexicon

def custom_sentiment_analysis(text):
    # Tokenize the text
    words = nltk.word_tokenize(text.lower())
    sentiment_score = 0
    # Calculate the sentiment score using the VADER lexicon
    for word in words:
        if word in vader_lexicon:
            sentiment_score += vader_lexicon[word]
    return sentiment_score

# MongoDB connection and data retrieval setup
uri = "mongodb+srv://plin11:2968peter@cluster0.jwnt1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["test"]
collection = db["database"]

try:
    tweets_data = collection.find({}, {
        'tweet': 1,
        'likes': 1,
        'retweet_count': 1,
        'state_code': 1
    })
    data = [{
        'tweet': tweet.get('tweet', ''),
        'likes': tweet.get('likes', 0),
        'retweets': tweet.get('retweet_count', 0),
        'state_code': tweet.get('state_code', 'Unknown')
    } for tweet in tweets_data if tweet.get('state_code', 'Unknown') in us_state_codes]

    # Load data into DataFrame
    df = pd.DataFrame(data)
    print(f"Retrieved {len(df)} documents.")

    # Apply custom sentiment analysis to each tweet
    df['sentiment_score'] = df['tweet'].apply(custom_sentiment_analysis)

    # Classify sentiment based on the score
    df['sentiment_category'] = df['sentiment_score'].apply(
        lambda score: 'positive' if score > 0.1 else ('negative' if score < -0.1 else 'neutral')
    )

    # Group by state and sentiment category and summarize
    summary = df.groupby(['state_code', 'sentiment_category']).agg({
        'likes': 'mean',
        'retweets': 'mean',
        'sentiment_score': 'count'
    }).rename(columns={'sentiment_score': 'count'})

    # Prepare and print the table
    table = PrettyTable()
    table.field_names = ["State Code", "Sentiment Category", "Average Likes", "Average Retweets", "Count"]
    for index, row in summary.iterrows():
        table.add_row([index[0], index[1], round(row['likes'], 2), round(row['retweets'], 2), row['count']])
    print(table)
    # Create a stacked bar chart for likes and retweets by state
    state_engagement = df.groupby('state_code').agg({'likes': 'sum', 'retweets': 'sum'})
    plt.figure(figsize=(15, 10))
    state_engagement.plot(kind='bar', stacked=True)
    plt.title('Total Engagement by State (Likes and Retweets)')
    plt.xlabel('State Code')
    plt.ylabel('Total Count')
    plt.legend(title='Type of Engagement')
    plt.show()

    # Sentiment Distribution (Pie Graph)
    sentiment_counts = df['sentiment_category'].value_counts()
    plt.figure(figsize=(10, 8))
    plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title('Sentiment Distribution Across Tweets')
    plt.show()

    # Engagement vs Sentiment (Scatterplot)
    plt.figure(figsize=(15, 10))
    sns.scatterplot(data=df, x='sentiment_score', y='likes', hue='sentiment_category', style='sentiment_category', s=100)
    plt.title('Engagement vs. Sentiment Score')
    plt.xlabel('Sentiment Score')
    plt.ylabel('Likes')
    plt.grid(True)
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")
