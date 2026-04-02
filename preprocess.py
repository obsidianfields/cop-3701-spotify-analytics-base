import csv
import os
import random
from faker import Faker

fake = Faker()

# Create data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Configuration
INPUT_FILE = 'RawSongData.csv' # Your on-hand CSV file
NUM_USERS = 150 # Number of fictional users to generate
STREAMS_PER_USER = 10 # Average number of songs each user has listened to

song_ids = []
user_ids = []

print("1. Processing existing songs and assigning unique Song IDs...")
# Create processed CSV files
with open(INPUT_FILE, mode='r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    headers = next(reader)

    with open('data/songs.csv', mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        # Prepend 'Song_ID' to pre-existing headers
        writer.writerow(['Song_ID'] + headers)

        song_id_counter = 1
        for row in reader:
            writer.writerow([song_id_counter] + row)
            song_ids.append(song_id_counter)
            song_id_counter += 1

print(f"   -> Assigned IDs to {len(song_ids)} songs.")

print("2. Generating fictional users and unique emails...")
# Generate Users
with open('data/users.csv', mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['User_ID', 'Email_Address', 'User_Name'])

    for u_id in range(1, NUM_USERS + 1):
        user_ids.append(u_id)
        # Generate a guaranteed unique email and fictional username
        email = fake.unique.email()
        username = fake.user_name()
        writer.writerow([u_id, email, username])

print(f"   -> Generated {NUM_USERS} unique users.")

print("3. Generating fictional streaming history tying users to your real songs...")
# Generate User Streaming History
with open('data/user_streaming_history.csv', mode='w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['User_ID', 'Song_ID', 'Stream_Count', 'Last_Listened_Date'])

    seen_pairs = set()
    total_streams_generated = 0

    # Randomly assign songs to users
    for u_id in user_ids:
        # Give each user a random number of songs they've listened to
        num_songs_listened = random.randint(1, STREAMS_PER_USER * 2)

        for _ in range(num_songs_listened):
            s_id = random.choice(song_ids)

            # Ensure no violation of the composite primary key (User_ID, Song_ID)
            if (u_id, s_id) not in seen_pairs:
                stream_count = random.randint(1, 100)
                last_listened = fake.date_time_this_year().isoformat()

                writer.writerow([u_id, s_id, stream_count, last_listened])
                seen_pairs.add((u_id, s_id))
                total_streams_generated += 1

print(f"   -> Generated {total_streams_generated} unique streaming records.")
print("Processing complete. Files are ready in the 'data/' folder.")
