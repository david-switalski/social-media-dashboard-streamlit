# Social Media Analytics Dashboard

![Dashboard Demo](screenshots/dashboard.gif)

---

## Overview 
This project is a dynamic and interactive **Social Media Analytics Dashboard** built using Streamlit and Plotly. It provides an intuitive interface to explore and visualize tweet data, focusing on tweet volume, sentiment distribution, and key recurring words. The dashboard allows users to filter data by author and year, offering granular insights into tweeting patterns and public sentiment over time.

This application demonstrates strong data processing, visualization, and web application development skills in Python, making it a valuable addition to a data analyst or data scientist portfolio.

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

---

## Project Structure

The project follows a modular structure for improved organization, readability, and maintainability:

```bash
streamlit-dashboard/
├── data/
│   └── tweets.csv            # Original dataset
├── app.py                    # Main Streamlit application script
├── data_processing.py        # Module for data loading and preprocessing
├── plotting.py               # Module for all chart generation functions
├── utils.py                  # Module for helper functions (e.g., custom CSS, sentiment classification)
├── requirements.txt          # List of all project dependencies
├── README.md                 # Project documentation (this file)
└── screenshots/              # Folder for dashboard screenshots or GIFs
    └── dashboard_screenshot.png
    └── dashboard_demo.gif (optional)
```

---

## Installation and Setup

Follow these steps to set up and run the dashboard locally:

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/david-switalski/social-media-dashboard-streamlit.git](https://github.com/david-switalski/social-media-dashboard-streamlit.git)
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

* **Data Source**
    The tweet dataset used in this project was obtained from Kaggle:
    *Tweets Dataset by mmmarchetti*
    *URL: https://www.kaggle.com/datasets/mmmarchetti/tweets-dataset*

* **Contribution**
    You can submit a change contribution request if you want to contribute or improve a feature.

* **Contact**
    [David Switalski/[LinkedIn Profile](https://www.linkedin.com/in/david-switalski-50b11133a/)]
    Email: davidspuni@gmail.com
