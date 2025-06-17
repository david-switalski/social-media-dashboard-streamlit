import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except nltk.downloader.DownloadError:
    nltk.download('stopwords')
    
def display_author_monthly_tweet_volume_bar_chart(df, authorTweet, yearTweet):
    """
    Generates a bar chart showing the volume of tweets by month for a specific author and year.

    Args:
        df (pd.DataFrame): Filtered DataFrame containing tweet data.
        authorTweet (str): Autor's name for the title of the chart.
        yearTweet (int): Year for the title of the chart.

    Returns:
        plotly.graph_objects.Figure: Object of Plotly figure
    """
    df_merge = df.groupby('month', observed=False).size().reset_index(name='total')
    df_merge = df_merge.sort_values(by='month')
    fig = px.bar(df_merge, x='month', y='total', title=f'Tweet Volume by Month for {authorTweet} in {yearTweet}', color_discrete_sequence= ['#0210a5'])
    return fig

def display_total_tweets_by_author_pie_chart(df):
    """
    Generates a pie chart comparing the total number of tweets per author.

    Args:
        df (pd.DataFrame): DataFrame with all the tweet data.

    Returns:
        plotly.graph_objects.Figure: Object of Plotly figure
    """
    df_to_plot = df['author'].value_counts().reset_index()
    df_to_plot = df_to_plot.rename(columns={'total': 'author', 'count': 'total'})
    fig = px.pie(df_to_plot, values='total', names='author', title='Comparison of tweet numbers (2010-2017)')
    fig.update_layout(margin=dict(t=50, b=50, l=50, r=50))
    return fig

def display_word_cloud(df, authorTweet, yearTweet):
    """
    Displays a word cloud of tweets from a specific author and year.

    Args:
        df (pd.DataFrame): Filtered DataFrame containing tweet data.
        authorTweet (str): Autor's name for the title of the chart.
        yearTweet (int): Year for the title of the chart.

    Returns:
        matplotlib.figure.Figure or None: The Matplotlib figure of the word cloud, or None if there is no valid text.
    """
    if df.empty:
        st.warning(f'There is no valid tweet text for {authorTweet} in {yearTweet} to generate the word cloud.')
        return None

    all_words = ' '.join(df['tweet_text'].dropna().astype(str).tolist())
    manual_stopwords = [
        'the', 'and', 'to', 'of', 'a', 'in', 'is', 'it', 'that', 'this',
        'for', 'on', 'with', 'as', 'was', 'at', 'an', 'are',
    ]
    nltk_stopwords = set(stopwords.words('english'))
    all_combined_stopwords = set(manual_stopwords).union(nltk_stopwords)

    wordcloud = WordCloud(
        width=800, height=300, background_color='white',
        stopwords=all_combined_stopwords, min_font_size=10, max_words=100
    ).generate(all_words)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
    plt.close(fig)
    return fig

def display_author_monthly_sentiment_pie_chart(df, yearTweet):
    """
    Generates a pie chart showing the distribution of sentiment classes for tweets.

    Args:
        df (pd.DataFrame): Filtered DataFrame containing tweet data.
        yearTweet (int): Year for the title of the chart.

    Returns:
        plotly.graph_objects.Figure: Object of Plotly figure
    """
    df_to_plot = df['sentiment_class'].value_counts().reset_index()
    df_to_plot = df_to_plot.rename(columns={'sentiment_class': 'sentiment', 'count': 'total'})
    color_vibrant = ['#112cee', '#66b3ff', '#ee1111']
    fig = px.pie(df_to_plot, values='total', names='sentiment', title= f'Sentiment Distribution for {yearTweet}', color_discrete_sequence=color_vibrant)
    fig.update_layout(margin=dict(t=90, b=10, l=50, r=50))
    return fig

def display_author_monthly_sentiment_volume_line_chart(df, authorTweet, yearTweet):
    """
    Generates a line chart of the monthly average sentiment.

    Args:
        df (pd.DataFrame): Filtered DataFrame containing tweet data.
        authorTweet (str): Autor's name for the title of the chart.
        yearTweet (int): Year for the title of the chart.

    Returns:
        plotly.graph_objects.Figure: Object of Plotly figure
    """
    df_monthly_sentiment = df.groupby('month', observed=False)['sentiment'].mean().reset_index()
    df_monthly_sentiment.rename(columns={'sentiment': 'average_sentiment'}, inplace=True)
    df_monthly_sentiment['average_sentiment'] = df_monthly_sentiment['average_sentiment'].fillna(0)

    fig = px.line(
        df_monthly_sentiment, x='month', y='average_sentiment',
        title=f'Monthly Average Sentiment for {authorTweet} in {yearTweet}',
        labels={'month': 'Month', 'average_sentiment': 'Average Sentiment'},
        markers=True, color_discrete_sequence=['#1F77B4']
    )
    fig.add_trace(
        go.Scatter(
            x=df_monthly_sentiment['month'], y=df_monthly_sentiment['average_sentiment'],
            fill='tozeroy', fillcolor='rgba(100, 149, 237, 0.2)', showlegend=False
        )
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral", annotation_position="bottom right")
    fig.add_hline(y=0.5, line_dash="dash", line_color="green", annotation_text="Positive", annotation_position="bottom right")
    fig.add_hline(y=-0.5, line_dash="dash", line_color="red", annotation_text="Negative", annotation_position="bottom right")
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(range=[-1, 1])
    fig.update_layout(
        margin=dict(t=90, b=50, l=50, r=50),
        yaxis=dict(domain =[0, 0.94])
    )
    return fig