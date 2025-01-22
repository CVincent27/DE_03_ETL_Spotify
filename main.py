import pandas as pd
from extract import get_authorization_code, get_access_token, get_user_data, get_recent_tracks  
from transform import filter_recent_tracks  
from load import create_database, load_data_to_db  

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

# Main Function
if __name__ == '__main__':
    auth_code = get_authorization_code()  # 1.
    access_token = get_access_token(auth_code)  # 2.
    
    if access_token:
        user_data = get_user_data(access_token)  # 3.

        recent_tracks = get_recent_tracks(access_token)  # 4.
        if recent_tracks:
            print("Musiques récemment écoutées :")

            track_names = []
            artist_names = []
            played_ats = []

            for track in recent_tracks:
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                played_at = track['played_at']
                played_at = pd.to_datetime(played_at).strftime('%Y-%m-%d %H:%M:%S')
                track_names.append(track_name)
                artist_names.append(artist_name)
                played_ats.append(played_at)

            # Création df
            track_dict = {
                "track": track_names,
                "artist": artist_names,
                "played_at": played_ats
            }

            track_df = pd.DataFrame(track_dict, columns=["track", "artist", "played_at"])

            # filtre last 24h
            filtered_df = filter_recent_tracks(track_df)
            
            if not filtered_df.empty:
                print(filtered_df)
                print("Data validée")
                create_database() 
                load_data_to_db(filtered_df) 
            else:
                print("Aucune musique écoutée dans les 24 dernières heures.")
