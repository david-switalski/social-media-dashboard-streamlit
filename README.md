# Social Media Analytics Dashboard

![GitHub License](https://img.shields.io/github/license/david-switalski/social-media-dashboard-streamlit)

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-grey?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-23F2BC?style=flat&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![VaderSentiment](https://img.shields.io/badge/VaderSentiment-FF69B4?style=flat&logoColor=white)](https://github.com/cjhutto/vaderSentiment)
[![NLTK](https://img.shields.io/badge/NLTK-394F6A?style=flat&logo=nltk&logoColor=white)](https://www.nltk.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat&logo=matplotlib&logoColor=white)](https://matplotlib.org/)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-20BEFF?style=flat&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/mmmarchetti/tweets-dataset)
[![Deployed on Streamlit Cloud](https://img.shields.io/badge/Deployed%20on-Streamlit%20Cloud-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://social-media-dashboard-app-xpwxatitnjprnkp9v5cfde.streamlit.app/)

![dashboard](https://github.com/user-attachments/assets/ac2b90d5-f92d-409a-b03b-89e7cf4f7938)

---

## Overview 
This project is a dynamic and interactive **Social Media Analytics Dashboard** built using Streamlit and Plotly. It provides an intuitive interface to explore and visualize tweet data, focusing on tweet volume, sentiment distribution, and key recurring words. The dashboard allows users to filter data by author and year, offering granular insights into tweeting patterns and public sentiment over time.

---

## Features

* **Interactive Filtering:** Easily filter the displayed data by selecting specific authors and years from the sidebar.
* **Tweet Volume Analysis:** A bar chart visualizes the monthly tweet activity for the selected author and year, showing patterns and peaks.
* **Author Tweet Comparison:** A pie chart provides an overview of the total number of tweets contributed by each author across the entire dataset (2010-2017).
* **Sentiment Distribution:** A pie chart illustrates the breakdown of tweet sentiment (Positive, Negative, Neutral) for the filtered data, offering quick insights into the general tone.
* **Monthly Sentiment Trend:** A line chart tracks the average sentiment score month-over-month, allowing for the identification of sentiment shifts over time.
* **Word Cloud Generation:** A word cloud dynamically displays the most frequent words used in the filtered tweets, highlighting common themes and topics.
* **Clean and User-Friendly Interface:** Built with Streamlit's intuitive components and custom CSS for a polished look.

---

## Technologies Used

* **Python 3.x**
* **Streamlit:** For creating the interactive web application.
* **Pandas:** For data manipulation and analysis.
* **Plotly Express & Plotly Graph Objects:** For generating interactive and visually appealing charts.
* **VaderSentiment:** For rule-based sentiment analysis of tweet text.
* **WordCloud:** For generating visual word clouds.
* **NLTK (Natural Language Toolkit):** Used for managing stopwords in text processing.
* **Matplotlib:** Used in conjunction with WordCloud for rendering.
* **Regular Expressions (re):** For cleaning tweet text (removing URLs, mentions, hashtags).
* **Request:** To keep the "streamlit cloud" service active programmatically.

---

## Project Structure

The project follows a modular structure for improved organization, readability, and maintainability:

```bash
streamlit-dashboard/
    ├── .gitignore                # Specifies files/folders to be ignored by Git
    ├── data/
    │   └── tweets.csv            # Original dataset with tweets
    ├── request/
    │   └── http_request_handler.py   # Handles HTTP requests
    ├── screenshot/
    │   └── dashboard.gif         # Dashboard screenshot or GIF
    ├── __init__.py               # Marks directory as a Python package
    ├── app.py                    # Main Streamlit app entry point
    ├── config.py                 # App configuration settings
    ├── data_processing.py        # Data loading and preprocessing functions
    ├── LICENSE
    ├── plotting.py               # Chart and plot generation functions
    ├── utils.py                  # Helper utility functions
    ├── README.md                 # Project documentation
    └── requirements.txt          # Python dependencies list
```

---

## Installation and Setup

Follow these steps to set up and run the dashboard locally:

1. **Clone the repository:**
    ```bash
    git clone https://github.com/david-switalski/social-media-dashboard-streamlit.git
    cd social-media-dashboard-streamlit

2. **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv

3. **Activate the virtual environment:**
    
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Download NLTK stopwords (if not already downloaded):**
    Open a Python interpreter in your active virtual environment and run:
    ```python
    import nltk
    nltk.download('stopwords')
    ```
    This step is only required once.

---

## How to Run the App

After completing the installation and setup steps, ensure your virtual environment is activated and run the Streamlit application:

```bash
streamlit run app.py
```

The application will automatically open in your default web browser (usually at http://localhost:8501).

## Analyze an Xquik CSV Export

Use the sidebar uploader to load a saved Xquik CSV export. The data loader maps
common export headers such as `created_at`, `date`, `timestamp`, `text`,
`tweet`, `full_text`, `username`, `screen_name`, `likes`, `like_count`,
`retweets`, and `retweet_count` into the dashboard's existing tweet, author,
date, and engagement columns before running the VADER sentiment pipeline. Blank
tweet rows are skipped, and numeric engagement columns are coerced before charts
read them.

---

## Contact

**David Switalski**
*(Informático y Desarrollador en Formación)*

* **LinkedIn:** [David Switalski](https://www.linkedin.com/in/david-switalski-50b11133a/)
* **GitHub:** [David Switalski](https://github.com/david-switalski)
* **Email:** davidspuni@gmail.com

---

## Live Deployment

* **Web Application:** 
    This dashboard is professionally deployed on **Streamlit Cloud**:
    *URL: https://social-media-dashboard-app-xpwxatitnjprnkp9v5cfde.streamlit.app/*
* **Data Source:** 
    The tweet dataset used in this project was obtained from Kaggle:
    *Tweets Dataset by mmmarchetti*
    *URL: https://www.kaggle.com/datasets/mmmarchetti/tweets-dataset*

---

## Contribution

Contributions are welcome! Please feel free to submit a pull request or open an issue to discuss potential changes or additions.
