import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 as pg

DB_HOST= st.secrets['DB_HOST']
DB_PORT = st.secrets['DB_PORT']
DB_NAME = st.secrets['DB_NAME']
DB_USERNAME = st.secrets['DB_USERNAME']
DB_PASSWORD = st.secrets['DB_PASSWORD']

def fetch_data(query, params=None):
    conn = conn = pg.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD)
    try:
        if params:
        	results = pd.read_sql_query(query, conn, params)    
        else:
            results = pd.read_sql_query(query, conn)    
        return results
    finally:
        conn.close()
