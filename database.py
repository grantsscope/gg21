import streamlit as st
import pandas as pd
import numpy as np
import psycopg2 as pg



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
