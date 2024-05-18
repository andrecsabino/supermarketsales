import streamlit as st
import pandas as pd

#Page Configuration
st.set_page_config(
    layout='wide'
)


#Data Cash
@st.cache_data
def load_data(file):
    
    df = pd.read_csv(file, sep=',', decimal='.')
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
    return df

if 'data' not in st.session_state:
    st.session_state['data'] = load_data('./data/sales.csv')


with st.sidebar:
    st.caption('Desenvolvido por André Sabino')
    st.caption('📞 85 98549-2335')
    st.caption('📧 andresabino.85@gmail.com')
    st.caption('https://www.linkedin.com/in/andre-sabino-3a26a460/')


st.markdown('# SUPERMARKET SALES DATASET!🍞🧀🥩')



st.link_button(label='Acesse o dataset no kaggle', url='https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales')
st.link_button(label='Acesse o repositório do projeto', url='https://github.com/andrecsabino/supermarketsales')