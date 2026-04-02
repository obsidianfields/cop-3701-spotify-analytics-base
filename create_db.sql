-- Strong Entity: Genre
CREATE TABLE Genre (
    Genre_Name VARCHAR(50) PRIMARY KEY
);

-- Strong Entity: Artist
CREATE TABLE Artist (
    Artist_ID INT PRIMARY KEY,
    Artist_Name VARCHAR(100) NOT NULL,
    Middle_Name VARCHAR(100),
    Popularity_Rank INT
);

-- Strong Entity: User
CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
    Email_Address VARCHAR(255) UNIQUE NOT NULL,
    User_Name VARCHAR(100) NOT NULL
);

CREATE TABLE Song (
    Song_ID INT PRIMARY KEY,
    Song_Title VARCHAR(200) NOT NULL,
    Song_Duration INT,
    Total_Streams INT DEFAULT 0,
    Artist_ID INT NOT NULL,
    Genre_Name VARCHAR(50),
    FOREIGN KEY (Genre_Name) REFERENCES Genre(Genre_Name),
    FOREIGN KEY (Artist_ID) REFERENCES Artist(Artist_ID)
);

CREATE TABLE Account_Status (
    User_ID INT PRIMARY KEY,
    Subscription_Tier VARCHAR(20) DEFAULT 'Free',
    Last_Login TIMESTAMP,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
);

CREATE TABLE Subscription (
    Subscription_ID INT,
    User_ID INT,
    Start_Date DATE NOT NULL,
    End_Date DATE,
    PRIMARY KEY (Subscription_ID, User_ID),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE
);

CREATE TABLE Performance (
    Song_ID INT,
    Artist_ID INT,
    Contribution_Role VARCHAR(50),
    PRIMARY KEY (Song_ID, Artist_ID),
    FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID),
    FOREIGN KEY (Artist_ID) REFERENCES Artist(Artist_ID)
);

CREATE TABLE User_Streaming_History (
    User_ID INT,
    Song_ID INT,
    Stream_Count INT DEFAULT 1,
    Last_Listened_Date TIMESTAMP,
    PRIMARY KEY (User_ID, Song_ID),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID) ON DELETE CASCADE,
    FOREIGN KEY (Song_ID) REFERENCES Song(Song_ID) ON DELETE CASCADE
);

-- Initial sync of the denormalized column post-insertion targeting Song
UPDATE Song s
SET Total_Streams = (
    SELECT COALESCE(SUM(Stream_Count), 0)
    FROM User_Streaming_History ush
    WHERE ush.Song_ID = s.Song_ID
);

DELIMITER //
CREATE TRIGGER After_User_Stream_Update
AFTER UPDATE ON User_Streaming_History
FOR EACH ROW
BEGIN
    UPDATE Song
    SET Total_Streams = Total_Streams + (NEW.Stream_Count - OLD.Stream_Count)
    WHERE Song_ID = NEW.Song_ID;
END; //
DELIMITER ;
