# cop-3701-spotify-analytics-base
This analytics base aims to track various metrics for the streaming platform Spotify. Using a database of various songs across a diverse range of genres and artists, I aim to compare and contrast the popularity metrics over time for each genre, and, by extension, the most popular artists within each genre in terms of streaming count/popularity.

# Application
The database will be applied using streaming metrics from user emails. All accounts require a registered email to count towards a stream, and all emails are unique with unique IDs as well.
These users also possess subscriptions, which cannot exist without an associated User, this allows insight into Spotify Premium subscriptions. Playlists are also relevant metrics to track genres by, that can be either user-generated or from Spotify themselves, meaning that repeat streams of specific songs will also be accounted for on a per-user basis and its total will be calculated separately. Regardless, it will provide access to further genre metrics.
Songs, artists, and genres are tracked separately from user metrics for the purposes of clearly defining performance and rankings between artists and genres. Genres are dependent on songs, and a many-to-many relationship exists between artists and songs too for the purposes of tracking artist roles.

This database for the sake of more detailed inferences between stream count and other attributes, also includes things like song duration, dates of last login for users, and subscription tiers for analyzing the relationship between user preferences outside of just song genre.

It should be noted that the data source does not account for individuals' streaming metrics. Fictional metrics will be generated so as to demonstrate the functions of the database. This also means that any username and e-mail is entirely fictitious and any connections to real people are purely coincidental.

[ER Design](https://github.com/obsidianfields/cop-3701-spotify-analytics-base/blob/24d25a25e3c2ab7340ade08d1b0802dd5166c804/database_er.md)
# Data Sources:
https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db
