-- 3. Total Stream Count Temp Table
select 
    art.artist_name, 
    sum(ush.stream_count) as total_streams
from user_streaming_history ush
join song s on ush.song_id = s.song_id
join artist art on s.artist_id = art.artist_id 
where art.artist_name like :user_input
group by art.artist_id, art.artist_name;
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
select 
    u.user_name, 
    a.last_login
from users u
join account_status a using (user_id)
where u.user_name like :user_input
and a.last_login > '2026-01-01';