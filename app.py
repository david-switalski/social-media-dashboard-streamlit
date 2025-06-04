import streamlit as st
import pandas as pd
# import seaborn as sns

st.set_page_config(
    page_title="Social Media Analytics",
    page_icon=":bar_chart:",  
    layout="wide",  
    initial_sidebar_state="expanded" 
)

if 'df' not in st.session_state:
    st.session_state.df = None
    st.session_state.message = None
    
with st.sidebar:
    st.title("Social Media Analytics")
    
    if st.session_state.df is not None:
        yearTweet = st.selectbox('Año', options=st.session_state.df['date_time'].unique(), index=0)
    else:
        yearTweet = st.selectbox('Año', options=[], index=0)
        
            
    file_up = st.file_uploader("Select File", type=["csv","xlsx"], accept_multiple_files=False, help=("Formatos soportados: CSV o Excel"), label_visibility="visible")
    
    if file_up is not None and st.session_state.df is None:
        
        if file_up.name.endswith('.csv'):
            df = pd.read_csv(file_up)
        elif file_up.name.endswith('.xlsx'):
            df = pd.read_excel(file_up)
            
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
        
        st.session_state.message = f"File '{file_up.name}' uploaded successfully!"
        st.session_state.df = df
        st.rerun()
    elif file_up is None and st.session_state.df is not None:
        st.session_state.df = None
        st.session_state.message = "File removed successfully!"
        st.rerun()
            
    
    if st.session_state.message is not None:
        st.success(st.session_state.message)
        st.session_state.message = None
        
        
        
        
def main():
    st.title("Streamlit App")
   
main()