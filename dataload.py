import pandas as pd
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random

# Initialize Faker
fake = Faker()

db_config = {
    'host': 'localhost',
    'user': 'danirojas',
    'password': 'Dany12321!',
    'database': 'jorgebase'
}

def load_data(file_path):
    conn = None
    try:
        print(f"Reading {file_path}...")
        df = pd.read_csv(file_path, on_bad_lines='warn', engine='python', encoding='utf-8')
        df = df.where(pd.notnull(df), None)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("Connected to MariaDB.")

        # --- 1. LOAD GENRE, ARTIST, SONG (Your existing logic) ---
        # [Keeping your logic here but collecting IDs for foreign keys]
        
        # Genres
        unique_genres = df['genre'].dropna().unique()
        cursor.executemany("INSERT IGNORE INTO Genre (Genre_Name) VALUES (%s)", [(str(g),) for g in unique_genres])

        # Artists
        artist_df = df[['artist_name', 'popularity']].groupby('artist_name').max().reset_index()
        artist_df['artist_id'] = range(1, len(artist_df) + 1)
        artist_map = dict(zip(artist_df['artist_name'], artist_df['artist_id']))
        artist_data = [(r['artist_id'], str(r['artist_name'])[:255], None, int(r['popularity'] or 0)) for _, r in artist_df.iterrows()]
        cursor.executemany("INSERT IGNORE INTO Artist (Artist_ID, Artist_Name, Middle_Name, Popularity_Rank) VALUES (%s, %s, %s, %s)", artist_data)

        # Songs
        unique_songs = df.drop_duplicates(subset=['track_id']).copy()
        unique_songs['song_int_id'] = range(1, len(unique_songs) + 1)
        song_ids = unique_songs['song_int_id'].tolist() # Saved for history generation
        
        song_data = []
        for _, row in unique_songs.iterrows():
            song_data.append((row['song_int_id'], str(row['track_name'])[:200], int(row['duration_ms'] or 0), 0, artist_map.get(row['artist_name']), row['genre']))
        cursor.executemany("INSERT IGNORE INTO Song (Song_ID, Song_Title, Song_Duration, Total_Streams, Artist_ID, Genre_Name) VALUES (%s, %s, %s, %s, %s, %s)", song_data)

        # --- 2. GENERATE USERS (Faker) ---
        print("Generating Users and Account Data...")
        num_users = 500
        user_ids = list(range(1, num_users + 1))
        users_list = []
        account_status_list = []
        subscription_list = []

        for uid in user_ids:
            # Users Table
            first = fake.first_name()
            last = fake.last_name()
            users_list.append((uid, f"{first.lower()}.{last.lower()}@example.com", f"{first} {last}"))
            
            # Account_Status Table
            tier = random.choice(['Free', 'Premium', 'Family', 'Student'])
            account_status_list.append((uid, tier, fake.date_time_this_year()))

            # Subscription Table
            start_date = fake.date_between(start_date='-2y', end_date='today')
            subscription_list.append((uid, uid, start_date, fake.date_between(start_date=start_date, end_date='+1y')))

        cursor.executemany("INSERT IGNORE INTO Users (User_ID, Email_Address, User_Name) VALUES (%s, %s, %s)", users_list)
        cursor.executemany("INSERT IGNORE INTO Account_Status (User_ID, Subscription_Tier, Last_Login) VALUES (%s, %s, %s)", account_status_list)
        cursor.executemany("INSERT IGNORE INTO Subscription (Subscription_ID, User_ID, Start_Date, End_Date) VALUES (%s, %s, %s, %s)", subscription_list)

        # --- 3. GENERATE STREAMING HISTORY (Faker) ---
        print("Generating Streaming History...")
        history_data = []
        # Create 5000 random "listens"
        for _ in range(5000):
            history_data.append((
                random.choice(user_ids),
                random.choice(song_ids),
                random.randint(1, 100), # Stream count
                fake.date_time_between(start_date='-1y', end_date='now') # Last_Listened_Date
            ))
        
        cursor.executemany("""
            INSERT IGNORE INTO User_Streaming_History (User_ID, Song_ID, Stream_Count, Last_Listened_Date) 
            VALUES (%s, %s, %s, %s)
        """, history_data)

        # --- 4. GENERATE PERFORMANCE (Mapping Songs to Artists) ---
        print("Processing Performances...")
        performance_data = [(row[0], row[4], 'Primary Artist') for row in song_data]
        cursor.executemany("INSERT IGNORE INTO Performance (Song_ID, Artist_ID, Contribution_Role) VALUES (%s, %s, %s)", performance_data)

        conn.commit()
        print("Success! All tables populated.")

    except Error as e:
        print(f"Database Error: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    load_data('SpotifyFeatures.csv')