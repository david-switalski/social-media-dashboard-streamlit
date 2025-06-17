import streamlit as st
from config import DATA_FILE_PATH
from data_processing import load_and_preprocess_data
from plotting import (
    display_author_monthly_tweet_volume_bar_chart,
    display_total_tweets_by_author_pie_chart,
    display_word_cloud,
    display_author_monthly_sentiment_pie_chart,
    display_author_monthly_sentiment_volume_line_chart
)
from utils import apply_custom_css

# Basic Streamlit App Configuration 
st.set_page_config(
    page_title="Social Media Analytics",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS styles from utils.py
apply_custom_css()

# Data Loading and Session State Initialization
if 'df' not in st.session_state:
    st.session_state.df = load_and_preprocess_data(DATA_FILE_PATH)

# Sidebar for Filtering Options
with st.sidebar:
    st.sidebar.header("Filters")
    authorTweet = None
    yearTweet = None

    if st.session_state.df is not None:
        # Get unique authors and sort them for the selectbox
        all_authors = sorted(st.session_state.df['author'].unique())
        authorTweet = st.selectbox('Author', options=all_authors, index=0, help="Select an author to filter the tweets.")

        # Filter the DataFrame by the selected author to get relevant years
        filtered_df_by_author = st.session_state.df[st.session_state.df['author'] == authorTweet]

        # Get unique years for the selected author and sort them
        if not filtered_df_by_author.empty:
            all_years = sorted(filtered_df_by_author['year'].unique())
            yearTweet = st.selectbox('Year', options=all_years, index=0, help="Select a year to filter the tweets.")
        else:
            st.warning("No data available for the selected author.")
            yearTweet = None 

# Main Dashboard Function
def main():
    """
    Main Streamlit application function that renders the dashboard.
    Displays various sentiment analysis and tweet volume charts
    based on user selections from the sidebar filters.
    """
    st.title("Social Media Analytics Dashboard")

    # Create columns for the overall dashboard layout
    col1_top, col_divider_top, col2_top = st.columns([0.45, 0.1, 0.45], vertical_alignment='center')
    st.markdown("---") # Horizontal divider
    col_mid, text_mid = st.columns([0.7, 0.3], vertical_alignment='center')
    st.markdown("---") # Horizontal divider
    col1_bottom, col_divider_bottom, col2_bottom = st.columns([0.45, 0.1, 0.45], vertical_alignment='top')

    # Proceed only if data is loaded and filters are selected
    if st.session_state.df is not None and authorTweet is not None and yearTweet is not None:
        df_filtered_for_display = st.session_state.df[
            (st.session_state.df['author'] == authorTweet) &
            (st.session_state.df['year'] == yearTweet)
        ]

        # Handle case where no data exists for the specific author and year combination
        if df_filtered_for_display.empty:
            st.warning(f"No tweet data available for **{authorTweet}** in **{yearTweet}**.")
            return 

        # Top Section: Bar Chart (Monthly Volume) & Pie Chart (Author Comparison in 2010-2017)
        with col1_top:
            fig_bar_chart = display_author_monthly_tweet_volume_bar_chart(df_filtered_for_display.copy(), authorTweet, yearTweet)
            fig_bar_chart.update_layout(height=400)
            st.plotly_chart(fig_bar_chart, use_container_width=True)

        with col_divider_top:
            st.markdown('<div class="vertical-divider" style="height: 400px;"></div>',
            unsafe_allow_html=True
            )

        with col2_top:
            fig_pie = display_total_tweets_by_author_pie_chart(st.session_state.df.copy())
            fig_pie.update_layout(height=352)
            st.plotly_chart(fig_pie, use_container_width=True)

        # Middle Section: Word Cloud and Description 
        with col_mid:
            display_word_cloud(df_filtered_for_display.copy(), authorTweet, yearTweet)

        with text_mid:
            st.markdown(
                """
                **Word Cloud for Tweets**: \n
                The word cloud above visualizes the most frequently used words in the tweets
                of the selected author for the specified year. Larger words indicate higher
                frequency, while smaller words are less common.
                """
            )

        # Bottom Section: Sentiment Distribution Pie Chart & Monthly Sentiment Line Chart
        with col1_bottom:
            fig_sentiment = display_author_monthly_sentiment_pie_chart(df_filtered_for_display.copy(), yearTweet)
            fig_sentiment.update_layout(height=400)
            st.plotly_chart(fig_sentiment, use_container_width=True)

            # Display sentiment counts for the filtered data
            total_tweets_filtered = df_filtered_for_display['tweet_text'].count()
            sentiment_counts = df_filtered_for_display['sentiment_class'].value_counts()
            positive_count = sentiment_counts.get('Positive', 0)
            negative_count = sentiment_counts.get('Negative', 0)
            neutral_count = sentiment_counts.get('Neutral', 0)

            st.markdown(f"""
                This **sentiment distribution chart** for **{authorTweet}** in **{yearTweet}**
                reveals the general tone of their tweets.

                From a total of **{total_tweets_filtered}** tweets in this period, they were classified as:
                - **Positive:** {positive_count} tweets
                - **Negative:** {negative_count} tweets
                - **Neutral:** {neutral_count} tweets
            """)

        with col_divider_bottom:
            st.markdown('<div class="vertical-divider" style="height: 600px;"></div>', unsafe_allow_html=True)

        with col2_bottom:
            fig_sentiment_line = display_author_monthly_sentiment_volume_line_chart(df_filtered_for_display.copy(), authorTweet, yearTweet)
            fig_sentiment_line.update_layout(height=500)
            st.plotly_chart(fig_sentiment_line, use_container_width=True)

        # Footer Section
        st.markdown("---")
        st.info("Social Media Analytics Dashboard | Developed with Streamlit and Plotly.")
        st.caption("Data (https://www.kaggle.com/datasets/mmmarchetti/tweets-dataset) | Visualizations with Plotly and WordCloud | Sentiment Analysis with VADER")

    else:
        # Error message if data could not be loaded or filters are not set
        st.error("The dashboard data could not be loaded! Please check the `tweets.csv` file.")
        st.info("Make sure 'data/tweets.csv' exists and is accessible.")


# Run the main application function 
if __name__ == "__main__":
    main()