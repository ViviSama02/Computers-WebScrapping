import streamlit as st
import pandas as pd

df = pd.read_csv('/home/sdvbigdata/SDV-DonneesDistribuees/products.csv')

st.text('Hello World')
st.dataframe(df)