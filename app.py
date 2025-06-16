import streamlit as st
import pandas as pd
import re 
import plotly.express as px
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords


st.set_page_config(
    page_title="Social Media Analytics",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    h1 {
        margin-top: 0px !important;
        margin-bottom: 30px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    
    h2 {
        margin-top: 0px;
        margin-bottom: 0px;
        padding-top: 0px;
        padding-bottom: 0px;
    }
    
    h3 {
        margin-top: 0px;
        margin-bottom: 0px;
        padding-top: 0px;
        padding-bottom: 0px;
    }
    
    </style>
    """, unsafe_allow_html=True)

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
        
        df['month'] = df['date_time'].dt.month_name()  
        orden_months = ['January', 'February', 'March', 'April', 'May', 'June',
                        'July', 'August', 'September', 'October', 'November', 'December']
        
        df['month'] = pd.Categorical(df['month'], categories=orden_months, ordered=True)
    else:
        df['year'] = None 
        df['month'] = None

    
    df['tweet_text'] = df['tweet_text'].astype('string')  
    
    # Remove URLs, mentions, hashtags, emojis, and special characters
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'http\S+|www\S+|https\S+','', x))
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'@\w+', '', x))
    df['tweet_text'] = df['tweet_text'].apply(lambda x: re.sub(r'#(\w+)', r'\1', x))
    
    df['tweet_text'] = df['tweet_text'].str.replace(r'\s+', ' ', regex=True).str.strip()
  
  
    analyzer = SentimentIntensityAnalyzer()
    
    df['sentiment'] = df['tweet_text'].apply(lambda x: analyzer.polarity_scores(x)['compound'])
    
    def classify_sentiment(compound_score):
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    df['sentiment_class'] = df['sentiment'].apply(classify_sentiment)  
   
    return df


if 'df' not in st.session_state:
    st.session_state.df = load_preloaded_data(DATA_FILE_PATH) 


with st.sidebar:
    st.sidebar.header("Filters")
    authorTweet = None
    yearTweet = None
    if st.session_state.df is not None:
        authorTweet = st.selectbox('Author', options=sorted(st.session_state.df['author'].unique()), index=0, help="Select an author to filter the tweets.")
        
        filtered_df_by_author = st.session_state.df[st.session_state.df['author'] == authorTweet]
        
        yearTweet = st.selectbox('Year', options=sorted(filtered_df_by_author['year'].unique()), index=0, help = "Select a year to filter the tweets.")
        
        
        
def display_author_monthly_tweet_volume_bar_chart(df, authorTweet, yearTweet): 
    df = df[df['author'] == authorTweet]
    df = df[df['year'] == yearTweet]
   
    df_merge = df.groupby('month', observed=False).size().reset_index(name='total')
    df_merge = df_merge.sort_values(by='month')
    
    fig = px.bar(df_merge, x='month', y='total', title=f'Tweet Volume by Month for {authorTweet} in {yearTweet}',)
    return fig


def display_total_tweets_by_author_pie_chart(df):    
    df_to_plot = df['author'].value_counts().reset_index()
    df_to_plot = df_to_plot.rename(columns={
        'total': 'author', 
        'count': 'total'
    })
    
    
    fig = px.pie(df_to_plot, values='total', names='author', title='Comparison of tweet numbers (2010-2017)')
    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
    return fig



def display_word_cloud(df, authorTweet, yearTweet):
    df_filtered = df[df['author'] == authorTweet]
    df_filtered = df_filtered[df_filtered['year'] == yearTweet]

    if df_filtered.empty:
        st.warning(f"No hay tweets para {authorTweet} en {yearTweet} para generar la nube de palabras.")
        return None

   
    all_words = ' '.join(df_filtered['tweet_text'].dropna().astype(str).tolist())

    manual_stopwords = [
        'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'that', 'this',
        'for', 'on', 'with', 'as', 'was', 'at', 'an', 'are',
        
    ]

   
    nltk_stopwords = set(stopwords.words('english')) 

    all_combined_stopwords = set(manual_stopwords).union(nltk_stopwords)

    
    if not all_words.strip():
        st.warning(f"No hay texto válido de tweets para {authorTweet} en {yearTweet} para generar la nube de palabras.")
        return None

    
    wordcloud = WordCloud(
        width=800,           
        height=400,         
        background_color='white', 
        stopwords=all_combined_stopwords,     
        min_font_size=10,    
        max_words=100        
    ).generate(all_words)

   
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear') 
    ax.axis('off') 

    st.pyplot(fig) 
    plt.close(fig) 

    return fig


def display_author_monthly_sentiment_chart(df, yearTweet, authorTweet):
    df = df[df['author'] == authorTweet]
    df = df[df['year'] == yearTweet]
    
    df_to_plot = df['sentiment_class'].value_counts().reset_index()
    df_to_plot = df_to_plot.rename(columns={
        'sentiment_class': 'sentiment',
        'count': 'total'
    })
    
    fig = px.pie(df_to_plot, values='total', names='sentiment', title= f'Sentiment Distribution for {yearTweet}')
    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
    return fig




def display_author_monthly_sentiment_volume_line_chart(df, authorTweet, yearTweet):
    df = df[df['author'] == authorTweet]
    df = df[df['year'] == yearTweet] 
    
    df_monthly_sentiment = df.groupby('month', observed=False)['sentiment'].mean().reset_index()

    df_monthly_sentiment.rename(columns={'sentiment': 'average_sentiment'}, inplace=True)

    df_monthly_sentiment['average_sentiment'] = df_monthly_sentiment['average_sentiment'].fillna(0)

    fig = px.line(
        df_monthly_sentiment,
        x='month',
        y='average_sentiment', 
        title=f'Tendencia del Sentimiento Promedio Mensual para {authorTweet} en {yearTweet}',
        labels={'month': 'Mes', 'average_sentiment': 'Sentimiento Promedio'},
        markers=True 
    )


    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral", annotation_position="bottom right")

    fig.update_yaxes(range=[-1, 1])
    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))

    return fig



def main():
    st.title("Social Media Analytics Dashboard")
    
    col1_top, col_divider, col2_top = st.columns([0.45,0.1, 0.45], vertical_alignment='center')
    
    with col1_top:
            if st.session_state.df is not None and authorTweet is not None and yearTweet is not None:
                fig_bar_chart = display_author_monthly_tweet_volume_bar_chart(st.session_state.df.copy(), authorTweet, yearTweet)
                fig_bar_chart.update_layout(height=448)
                st.plotly_chart(fig_bar_chart, use_container_width=True)
            
    with col_divider:
        st.markdown(
        """
        <style>
        .vertical-divider {
            border-left: 2px solid #ccc; 
            height: 400px; 
            width: 2px; 
            margin-left: auto; 
            margin-right: auto; 
            
            display: flex;
            justify-content: center; 
            align-items: center; 
        }
        </style>
        <div class="vertical-divider"></div>
        """,
        unsafe_allow_html=True
        )
        
    with col2_top:
        if st.session_state.df is not None:
            fig_pie = display_total_tweets_by_author_pie_chart(st.session_state.df.copy())
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        
    st.markdown("---")
    
    
    col_mid, text_mid = st.columns([0.7,0.3], vertical_alignment='center')
    
    
    with col_mid:
        if st.session_state.df is not None and yearTweet is not None and authorTweet is not None:
            display_word_cloud(st.session_state.df.copy(), authorTweet, yearTweet)
    
    with text_mid:    
        st.text("**Word Cloud**")
        st.markdown(
            """
            The word cloud above visualizes the most frequently used words in the tweets of the selected author for the specified year. 
            Larger words indicate higher frequency, while smaller words are less common.
            """
        )
    
    
    st.markdown("---")
    
    col1_bottom, col2_bottom= st.columns(2, vertical_alignment='center')
            
    with col1_bottom:
        if st.session_state.df is not None and yearTweet is not None and authorTweet is not None:
            fig_sentiment = display_author_monthly_sentiment_chart(st.session_state.df.copy(), yearTweet, authorTweet)
            fig_sentiment.update_layout(height=400)
            st.plotly_chart(fig_sentiment, use_container_width=True)
    
            
    with col2_bottom:
        if st.session_state.df is not None and yearTweet is not None and authorTweet is not None:
            fig_sentiment_line = display_author_monthly_sentiment_volume_line_chart(st.session_state.df.copy(), authorTweet, yearTweet)
            fig_sentiment_line.update_layout(height=400)
            st.plotly_chart(fig_sentiment_line, use_container_width=True)
    
    
if __name__ == "__main__":
    main()