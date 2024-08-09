import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DB_HOST= st.secrets['DB_HOST']
DB_PORT = st.secrets['DB_PORT']
DB_NAME = st.secrets['DB_NAME']
DB_USERNAME = st.secrets['DB_USERNAME']
DB_PASSWORD = st.secrets['DB_PASSWORD']

engine = create_engine(f'postgresql+pg8000://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def fetch_data(query, params=None):
    with engine.connect() as conn:
        if params:
            results = pd.read_sql_query(query, conn, params=params)
        else:
            results = pd.read_sql_query(query, conn)
        return results
