import pandas as pd
import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'danirojas',
    'password': 'Dany12321!',
    'database': 'jorgebase'
}

def load_data(file_path):
    conn = None
    try:
        # 1. LOAD DATA WITH SCHEMA FLEXIBILITY
        print(f"Reading {file_path}...")
        
        # We explicitly name columns to handle the shift at line 231718
        # and use 'on_bad_lines' to skip rows that are completely mangled.
        df = pd.read_csv(
            file_path, 
            on_bad_lines='warn', 
            engine='python',
            encoding='utf-8'
        )
        
        # Replace NaN with None (NULL in MySQL)
        df = df.where(pd.notnull(df), None)

        # 2. CONNECT TO MARIADB
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MariaDB.")

        # --- 3. LOAD GENRE ---
        print("Processing Genres...")
        # Ensure genre is a string and handle potential None values
        unique_genres = df['genre'].dropna().unique()
        genre_data = [(str(g),) for g in unique_genres]
        cursor.executemany("INSERT IGNORE INTO Genre (Genre_Name) VALUES (%s)", genre_data)

        # --- 4. LOAD ARTIST ---
        print("Processing Artists...")
        # Grouping by artist to find their max popularity rank
        artist_df = df[['artist_name', 'popularity']].groupby('artist_name').max().reset_index()
        artist_df['artist_id'] = range(1, len(artist_df) + 1)
        
        # Dictionary for fast lookup when loading Songs
        artist_map = dict(zip(artist_df['artist_name'], artist_df['artist_id']))
        
        artist_data = []
        for _, row in artist_df.iterrows():
            artist_data.append((
                row['artist_id'], 
                str(row['artist_name'])[:255], 
                None, 
                int(row['popularity']) if row['popularity'] is not None else 0
            ))
        
        cursor.executemany("""
            INSERT IGNORE INTO Artist (Artist_ID, Artist_Name, Middle_Name, Popularity_Rank) 
            VALUES (%s, %s, %s, %s)
        """, artist_data)

        # --- 5. LOAD SONG ---
        print("Processing Songs...")
        unique_songs = df.drop_duplicates(subset=['track_id']).copy()
        unique_songs['song_int_id'] = range(1, len(unique_songs) + 1)
        
        song_data = []
        for _, row in unique_songs.iterrows():
            # Get the Foreign Key (Artist_ID)
            a_id = artist_map.get(row['artist_name'])
            
            # SAFE STRING HANDLING: Prevents 'float not subscriptable' error
            track_name = str(row['track_name']) if row['track_name'] is not None else "Unknown"
            
            # (Song_ID, Song_Title, Song_Duration, Total_Streams, Artist_ID, Genre_Name)
            song_data.append((
                row['song_int_id'], 
                track_name[:200], # Trim to VARCHAR(200)
                int(row['duration_ms']) if row['duration_ms'] is not None else 0, 
                0, # Initial count
                a_id, 
                row['genre']
            ))

        cursor.executemany("""
            INSERT IGNORE INTO Song (Song_ID, Song_Title, Song_Duration, Total_Streams, Artist_ID, Genre_Name) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, song_data)

        # 6. COMMIT CHANGES
        conn.commit()
        print(f"Success! Loaded {cursor.rowcount} rows into the Song table.")

    except Error as e:
        print(f"Database Error: {e}")
    except Exception as e:
        print(f"Python Logic Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    load_data('SpotifyFeatures.csv')