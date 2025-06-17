import pandas as pd
import streamlit as st
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import classify_sentiment 

@st.cache_data
def load_and_preprocess_data(file_path):
    """
    Uploads a CSV file, preprocesses it for tweet analysis, and performs sentiment analysis.

    Rename columns, filter English tweets, remove unnecessary columns,
    process dates, clean tweet text (URLs, mentions, hashtags, spaces),
    and calculate and classify sentiment using VADER.

    Args:
        file_path (str): The path to the CSV file containing the tweet data.

    Returns:
        pandas.DataFrame or None: A cleaned, preprocessed DataFrame with the classified sentiment, or None if an error occurs.
    """
    try:
        df = pd.read_csv(file_path)

        df.rename(columns = {
            'content': 'tweet_text',
            'date_time': 'date_time',
            'number_of_likes': 'likes_count',
            'number_of_shares': 'retweet_count'
        }, inplace=True)

        df = df[df['language'] == 'en']

        df = df.drop(columns=[
            'id', 'language', 'latitude', 'longitude', 'country'
        ], errors='ignore')

        if 'date_time' in df.columns:
            df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce')
            df['year'] = df['date_time'].dt.year.astype('Int64')
            df = df.dropna(subset=['year'])

            df['month'] = df['date_time'].dt.month_name()
            orden_months = ['January', 'February', 'March', 'April', 'May', 'June',
                            'July', 'August', 'September', 'October', 'November', 'December']
            df['month'] = pd.Categorical(df['month'], categories=orden_months, ordered=True)
        else:
            df['year'] = None
            df['month'] = None

        df['tweet_text'] = df['tweet_text'].astype('string')

        df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+','', x))
        df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'@\w+', '', x))
        df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'#(\w+)', r'\1', x))
        df['tweet_text'] = df['tweet_text'].str.replace(r'\s+', ' ', regex=True).str.strip()

        analyzer = SentimentIntensityAnalyzer()
        df['sentiment'] = df['tweet_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
        df['sentiment_class'] = df['sentiment'].apply(classify_sentiment) 

        return df

    except FileNotFoundError:
        st.error(f"File not found: {file_path}. Make sure the file exists.")
        return None
    except Exception as e:
        st.error(f"Error loading or processing data: {e}")
        return None