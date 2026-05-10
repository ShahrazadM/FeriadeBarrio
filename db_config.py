import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

# Cargar .env solo si existe (modo local)
load_dotenv()

def get_connection():
    """Conexión a Neon (funciona en local y en la nube)"""
    
    # Intentar obtener credenciales de Streamlit Cloud primero
    try:
        conn = psycopg2.connect(
            host=st.secrets["NEON_DB_HOST"],
            port=st.secrets["NEON_DB_PORT"],
            dbname=st.secrets["NEON_DB_NAME"],
            user=st.secrets["NEON_DB_USER"],
            password=st.secrets["NEON_DB_PASSWORD"],
            sslmode="require"
        )
    except:
        # Si falla, usar variables de entorno (modo local)
        conn = psycopg2.connect(
            host=os.getenv("NEON_DB_HOST"),
            port=os.getenv("NEON_DB_PORT"),
            dbname=os.getenv("NEON_DB_NAME"),
            user=os.getenv("NEON_DB_USER"),
            password=os.getenv("NEON_DB_PASSWORD"),
            sslmode="require"
        )
    return conn

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)