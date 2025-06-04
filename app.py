import streamlit as st
import pandas as pd
import re 
# import matplotlib.pyplot as plt
# import seaborn as sns

st.set_page_config(
    page_title="Social Media Analytics",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE_PATH = "data/tweets.csv" 

@st.cache_data
def load_preloaded_data(file_path):
  
    df = pd.read_csv(file_path)
    
    # Processing and cleaning the data
    df.rename(columns = {
        'content': 'tweet_text',
        'date_time': 'date_time',
        'number_of_likes': 'likes_count',
        'number_of_shares': 'retweet_count'
    }, inplace=True)
    
    # Filter for English tweets
    df = df[df['language'] == 'en']
    
    # Delete unnecessary columns
    df = df.drop(columns=[
        'id',
        'language',
        'latitude',
        'longitude',
        'country'
    ], errors='ignore')
    
    # Convert 'date_time' to datetime and extract year
    if 'date_time' in df.columns:
        df['date_time'] = pd.to_datetime(df['date_time'], errors='coerce') 
        df['year'] = df['date_time'].dt.year.astype('Int64') 
        df = df.dropna(subset=['year']) 
    else:
        df['year'] = None 

    df['tweet_text'] = df['tweet_text'].str.lower().astype('string')  
    
    # Remove URLs, mentions, hashtags, emojis, and special characters
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+','', x))
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'@\w+', '', x))
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'#\w+', '' , x))
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]+', '', x))
    
    df['tweet_text'] = df['tweet_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
  
    return df


if 'df' not in st.session_state:
    st.session_state.df = load_preloaded_data(DATA_FILE_PATH) 

    
with st.sidebar:
    if st.session_state.df is not None:
        authorTweet = st.selectbox('Author', options=sorted(st.session_state.df['author'].unique()), index=0, help="Select an author to filter the tweets.")
        yearTweet = st.selectbox('Year', options=sorted(st.session_state.df['year'].unique()), index=0, help = "Select a year to filter the tweets.") 
          
  
def main():
    st.title("Social Media Analytics Dashboard")
    
    
if __name__ == "__main__":
    main()