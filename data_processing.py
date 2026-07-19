import pandas as pd
import streamlit as st
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from utils import classify_sentiment 

def get_column(df, names, default):
    for name in names:
        if name in df.columns:
            return df[name].fillna(default)
    return pd.Series([default] * len(df), index=df.index)

def normalize_tweet_columns(df):
    """
    Maps saved Xquik-style exports into the Kaggle dataset columns used by the dashboard.
    """
    if 'content' not in df.columns:
        df['content'] = get_column(df, ['text', 'tweet', 'full_text', 'body'], '')
    if 'date_time' not in df.columns:
        df['date_time'] = get_column(df, ['created_at', 'date', 'timestamp'], '')
    if 'author' not in df.columns:
        df['author'] = get_column(df, ['author', 'username', 'screen_name', 'user'], 'Xquik export')
    if 'language' not in df.columns:
        df['language'] = get_column(df, ['lang'], 'en')
    if 'number_of_likes' not in df.columns:
        df['number_of_likes'] = get_column(df, ['likes', 'like_count', 'favorite_count'], 0)
    if 'number_of_shares' not in df.columns:
        df['number_of_shares'] = get_column(df, ['retweets', 'retweet_count', 'shares'], 0)
    return df

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
        df = normalize_tweet_columns(df)

        df.rename(columns = {
            'content': 'tweet_text',
            'date_time': 'date_time',
            'number_of_likes': 'likes_count',
            'number_of_shares': 'retweet_count'
        }, inplace=True)

        for metric_column in ['likes_count', 'retweet_count']:
            if metric_column in df.columns:
                df[metric_column] = pd.to_numeric(df[metric_column], errors='coerce').fillna(0).astype('Int64')

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

        df['tweet_text'] = df['tweet_text'].astype('string').fillna('')
        df = df[df['tweet_text'].str.strip() != ''].copy()

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
