import pandas as pd
from connection import connection

def get_album(data):
    album_id=[]
    album_name=[]
    album_release_date=[]
    album_total_tracks=[]
    album_urls=[]
    for album in data["items"]:
        album_id.append(album["track"]["album"]["id"])
        album_name.append(album["track"]["album"]["name"])
        album_release_date.append(album["track"]["album"]["release_date"])
        album_total_tracks.append(album["track"]["album"]["total_tracks"])
        album_urls.append(album["track"]["album"]["external_urls"]["spotify"])
        album_dict={
            "album_id": album_id,
            "album_name":album_name,
            "album_release_date":album_release_date,
            "album_total_tracks":album_total_tracks,
            "album_urls":album_urls
        }
    return pd.DataFrame(album_dict)

def get_artist(data):
    artist_id=[]
    artist_name=[]
    artist_url=[]
    for artist_data in data["items"]:
        for key, value in artist_data.items():
            if key=="track":
                for artist in value["artists"]:
                    artist_id.append(artist["id"])
                    artist_name.append(artist["name"])
                    artist_url.append(artist["href"])
                    artist_dict={
                        "artist_id":artist_id,
                        "artist_name":artist_name,
                        "artist_href":artist_url
                    }
    return pd.DataFrame(artist_dict)


def get_songs(data):
    track_id=[]
    track_name=[]
    track_duration=[]
    track_url=[]
    track_popularity=[]
    album_id=[]
    artist_id=[]
    for song in data["items"]:
        track_id.append(song["track"]["id"])
        track_name.append(song["track"]["name"])
        track_duration.append(song["track"]["duration_ms"])
        track_url.append(song["track"]['external_urls']['spotify'])
        track_popularity.append(song["track"]["popularity"])
        album_id.append(song["track"]["album"]["id"])
        artist_id.append(song['track']['album']['artists'][0]['id'])
        song_dict={
            "track_id":track_id,
            "track_name":track_name,
            "track_duration":track_duration,
            "track_url":track_url,
            "track_popularity":track_popularity,
            "album_id":album_id,
            "artist_id":artist_id,
        }
    return pd.DataFrame(song_dict)


# Check Quality
def check_quality(data):
    if data.empty:
        print("Data Frame Is Empty")
        return False
    else:
        print("Null Not Found")

    if data.isnull().values.any():
        raise Exception("Null Value Found")
    else:
        print("Null Not Found")

# Save CSV
def write_data_csv(data, file_name):
    data.to_csv("C://Users//User//Desktop//Airflow//{}.csv".format(file_name), index=False)




# Run All Funcitons
def processes():
    album_data = get_album(connection())
    artist_data = get_artist(connection())
    song_data = get_songs(connection())
    data_ = [album_data, artist_data, song_data]
    file_names = ["album", "artist", "song"]
    for i, file_name in zip(data_, file_names):
        check_quality(i)
        write_data_csv(i, file_name)


