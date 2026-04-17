import streamlit as st
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "danirojas",
    "password": "Dany12321!",
    "database": "jorgebase",
    "port": 3306,  # Default MySQL port
}


try:
    print("Connecting to remote database...")
    global sqlconn
    global cur
    sqlconn = mysql.connector.connect(**DB_CONFIG)  # Connection to the MySQL DB
    cur = sqlconn.cursor()
except Exception as e:
    print("Failed To Connect...")
    print(e)
    exit(-1)


# Initialize the connection
conn = st.connection("mysql", type="sql")

st.title("🎵 Artist Stream Dashboard")

menu = ["Query1", "Query2", "Query3", "Query4", "Query5"]
choice = st.sidebar.selectbox("Select Query", menu)

query1 = (
    "select * from song where genre_name like :user_input order by genre_name desc;"
)
query2 = "select count(artist_name) from artist where artist_name like :user_input;"
query3 = """
select 
    art.artist_name, 
    sum(ush.stream_count) as total_streams
from user_streaming_history ush
join song s on ush.song_id = s.song_id
join artist art on s.artist_id = art.artist_id 
where art.artist_name like :user_input
group by art.artist_id, art.artist_name;
"""
query4 = "select count(genre_name) from song where genre_name like :user_input;"
query5 = """
select 
    u.user_name, 
    a.last_login
from users u
join account_status a using (user_id)
where u.user_name like :user_input
and a.last_login > '2026-01-01';
"""

# Query Menu Selection
if choice == "Query1":
    st.subheader("See all songs that have a specific genre name")
    st.write("Insert a genre")
    genre = st.text_input("Genre:")

    if st.button("Run Query"):
        try:
            df = conn.query(query1, params={"user_input": f"%{genre}%"})
            if not df.empty:
                st.write("All songs under the above genre:")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Could not find any songs!")
        except Exception as e:
            print(f"could not execute sql query!\n {e}")
elif choice == "Query2":
    st.subheader("See a count of how many songs an artist has")
    st.write("Insert artist name:")
    artist = st.text_input("Artist:")

    if st.button("Run Query"):
        try:
            df = conn.query(query2, params={"user_input": f"%{artist}%"})
            st.metric(label="Artist's Song Count:", value=df.iloc[0, 0])
        except Exception as e:
            st.error("No Streams Found!")
            print("could not execute sql query!")
            print(e)
elif choice == "Query3":
    st.subheader("Display all the total streams under a specific artist")
    st.write("Insert artist name:")
    artist = st.text_input("Artist:")

    if st.button("Run Query"):
        try:
            df = conn.query(query3, params={"user_input": f"%{artist}%"})
            # Check if the dataframe has any data
            if not df.empty:
                st.metric(
                    label=f"{artist}'s Total Streams:", value=df.iloc[0, 1]
                )  # Index 1 is total_streams
            else:
                st.warning("No streams found for this artist.")
        except Exception as e:
            st.error(f"Query failed: {e}")
elif choice == "Query4":
    st.subheader("Select a genre to see how many songs there are of it")
    st.write("Insert a genre")
    genre = st.text_input("Genre: ")

    if st.button("Run Query"):
        try:
            df = conn.query(query4, params={"user_input": f"%{genre}%"})
            if not df.empty:
                st.metric(label="Total Genre Songs Found:", value=df.iloc[0, 0])
            else:
                st.warning("No songs found for that genre.")
        except Exception as e:
            st.error(f"Query failed: {e}")
elif choice == "Query5":
    st.subheader("Shows if someone subscription access is 'active'")
    st.write("A user is 'active' if they last logged in before 2026")
    st.write("insert username:")
    username = st.text_input("Username: ")

    if st.button("Run Query"):
        try:
            df = conn.query(query5, params={"user_input": f"%{username}%"})
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("User not active")
        except Exception as e:
            print("could not execute sql query!")
            print(e)
