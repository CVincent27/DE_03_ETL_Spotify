import sqlite3
import pandas as pd

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

def create_database():
    """
    Crée la table dans la base de données si elle n'existe pas déjà.
    """
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        track VARCHAR(200),
        artist VARCHAR(200),
        played_at VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """
    cursor.execute(sql_query)
    print("Database créée")
    conn.close()


def load_data_to_db(track_df):
    """
    Charge les données dans la base de données SQLite.
    """
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    for _, row in track_df.iterrows():
        # S'assurer que played_at est bien une chaîne formatée
        played_at = pd.to_datetime(row['played_at']).strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
        INSERT OR REPLACE INTO my_played_tracks (track, artist, played_at)
        VALUES (?, ?, ?)
        """, (row['track'], row['artist'], played_at))

    conn.commit()
    conn.close()

    print("Data chargée dans la base")
