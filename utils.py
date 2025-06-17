import streamlit as st

def apply_custom_css():
    """Apply custom CSS styles to the Streamlit app."""
    st.markdown(
        """
        <style>
        h1 { margin-top: 0px !important; margin-bottom: 30px !important; padding-top: 0px !important; padding-bottom: 0px !important; }
        h2 { margin-top: 0px !important; margin-bottom: 0px !important; padding-top: 0px !important; padding-bottom: 0px !important; }
        h3 { margin-top: 0px !important; margin-bottom: 0px !important; padding-top: 0px !important; padding-bottom: 0px !important; }
        .vertical-divider {
            border-left: 2px solid #ccc;
            width: 2px;
            margin-left: auto;
            margin-right: auto;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
        """, unsafe_allow_html=True)
    
def classify_sentiment(compound_score):
    """
    Classifies a composite sentiment score into 'Positive', 'Negative', or 'Neutral'.

    Args:
        compound_score (float): The composite sentiment score obtained from the VADER analysis.

    Returns:
        str: The sentiment class ('Positive', 'Negative', 'Neutral').
    """
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'