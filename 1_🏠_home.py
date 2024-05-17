import streamlit as st
import pandas as pd

#Page Configuration
st.set_page_config(
    layout='wide'
)


#Data Cash
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, sep=',', decimal='.', date_format='%d/%m/%Y')
    return df

if 'data' not in st.session_state:
    st.session_state['data'] = load_data('./data/sales.csv')




st.markdown('# SUPERMARKET SALES DATASET!🍞🧀🥩')
st.link_button(label='Acesse o dataset no kaggle', url='https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales')