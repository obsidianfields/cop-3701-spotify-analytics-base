-- 3. Total Stream Count Temp Table
select 
    s.artist_id, 
    sum(ush.stream_count) as total_streams
from 
    user_streaming_history ush
join 
    song s on ush.song_id = s.song_id
where 
    s.artist_id like " "
group by 
    s.artist_id;

--1. Genre Alphabetical Order
select genre_name from song
where genre_name like " "
order by genre_name desc;

--2. Artist count selection
select count(aritist_name) from artist
where aritst_name like " ";

--4. Count songs under a genre
select count(genre_name) from song
where genre_name like " ";

--5 User is active
select u.user_name, u.last_listened_date from users u
join account_status a
using (song_id)
where u.user_name like " "
and last_listened_date > "2024-01-01";
