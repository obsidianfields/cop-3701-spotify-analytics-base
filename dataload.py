import csv
import mysql.connector
from mysql.connector import Error



DB_CONFIG = {
    'host': 'db.freesql.com',
    'user': 'username',
    'password': 'password',
    'database': 'database_name',
    'port': 3306 # Default MySQL port
}

def load_data_from_csv(connection, table_name, csv_file_path, insert_query):
    """Reads a CSV and batch inserts the data into the remote database."""
    print(f"Preparing to load data into {table_name} from {csv_file_path}...")

    try:
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader) # Skip header row

            data_to_insert = []
            for row in reader:
                # Convert empty strings to None so they become NULL in the database
                cleaned_row = tuple(None if val == '' else val for val in row)
                data_to_insert.append(cleaned_row)


            cursor = connection.cursor()

            cursor.executemany(insert_query, data_to_insert)
            connection.commit()

            print(f"   -> Successfully inserted {cursor.rowcount} rows into {table_name}.")
            cursor.close()

    except FileNotFoundError:
        print(f"   -> ERROR: File {csv_file_path} not found. Skipping.")
    except Error as e:
        print(f"   -> DATABASE ERROR inserting into {table_name}: {e}")
        connection.rollback() # Rollback on error to maintain data integrity

def main():
    connection = None
    try:
        print("Connecting to remote database...")
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")

            # 2. Define INSERT queries
            # Ensure the order of %s matches the columns in files
            queries = {
                'Users': "INSERT INTO Users (User_ID, Email_Address, User_Name) VALUES (%s, %s, %s)",

                'Song': "INSERT INTO Song (Song_ID, Song_Title, Song_Duration, Total_Streams, Artist_ID, Genre_Name) VALUES (%s, %s, %s, %s, %s, %s)",

                'User_Streaming_History': "INSERT INTO User_Streaming_History (User_ID, Song_ID, Stream_Count, Last_Listened_Date) VALUES (%s, %s, %s, %s)"
            }

            # 3. Execute the loads in the correct order to respect Foreign Key constraints

            load_data_from_csv(connection, 'Users', 'data/users.csv', queries['Users'])

            load_data_from_csv(connection, 'Song', 'data/songs.csv', queries['Song'])

            load_data_from_csv(connection, 'User_Streaming_History', 'data/user_streaming_history.csv', queries['User_Streaming_History'])

    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    finally:
        # 4. Clean up the connection
        if connection and connection.is_connected():
            connection.close()
            print("Database connection closed.")

if __name__ == '__main__':
    main()
