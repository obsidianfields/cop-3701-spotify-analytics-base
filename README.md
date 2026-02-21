# cop-3701-spotify-analytics-base
This analytics base aims to track various metrics for the streaming platform Spotify. Using a database of various songs across a diverse range of genres and artists, I aim to compare and contrast the popularity metrics over time for each genre, and, by extension, the most popular artists within each genre in terms of streaming count/popularity.

# Application
The database will be applied using streaming metrics from user emails. All accounts require a registered email to count towards a stream, and all emails are unique with unique IDs as well.
These users also possess subscriptions, which cannot exist without an associated User, this allows insight into Spotify Premium subscriptions. Playlists are also relevant metrics to track genres by, that can be either user-generated or from Spotify themselves. Regardless, it will provide access to further genre metrics.
Songs, artists, and genres are tracked separately from user metrics for the purposes of clearly defining performance and rankings between artists and genres. Genres are dependent on songs, and a many-to-many relationship exists between artists and songs too for the purposes of tracking artist roles.

This database for the sake of more detailed inferences between stream count and other attributes, also includes things like song duration, dates of last login for users, and subscription tiers for analyzing the relationship between user preferences outside of just song genre.
# Data Sources:
https://www.kaggle.com/datasets/zaheenhamidani/ultimate-spotify-tracks-db
