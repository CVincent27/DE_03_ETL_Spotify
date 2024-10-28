import sqlite3
import requests
import base64
# import json
import pandas as pd
import sqlalchemy

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
# ID client
CLIENT_ID = '02da1b0fd5474dc08cb4266d9dd13ae7'
CLIENT_SECRET = '5675b5ae4f664c339f81df5e7eca79b9'
REDIRECT_URI = 'http://127.0.0.1:5500/'
SCOPE = 'user-read-private%20user-read-email%20user-read-recently-played'


# Vérification validité données
def check_data(df: pd.DataFrame) -> bool:
    # Check empty data
    if df.empty:
        print("Aucune data, fin du programme.")
        return False
    
    # Check clé primaire (played_at)
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Doublon dans la clé primaire")
    
    # Check valeurs null
    if df.isnull().values.any():
        raise Exception("Valeurs nulles trouvées")
    
    # Check timestamps last month
    last_month = pd.Timestamp.now() - pd.Timedelta(days=30) #30 jours
    last_month = last_month.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df['timestamps'].tolist()
    for timestamp in timestamps:
        if pd.to_datetime(timestamp) < last_month:
            raise Exception("Musiques écoutées il y a plus de 24h")
    return True

# 1. Obtention code d'autorisation
def get_authorization_code():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    print(f"Code d'authentification : {auth_url}")
    
    # Entrer le code d'autorisation
    auth_code = input("Entrez le code : ")
    return auth_code

# 2. Echange code contre token
def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    
    # Créez un en-tête d'autorisation
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Les données pour l'échange
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    token_info = response.json()
    
    if 'access_token' in token_info:
        return token_info['access_token']
    else:
        print("Erreur lors de l'obtention du token")
        print(token_info)
        return None

# 3. token pour accéder à la data utilisateur
def get_user_data(access_token):
    user_url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(user_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
    else:
        print("Erreur:", response.status_code)
        print(response.text)
        return None

    # user_data = response.json()

    # Extraction data utilisateur
    if user_data:
        display_name = user_data.get('display_name', 'N/A')
        external_urls = user_data.get('external_urls', {}).get('spotify', 'N/A')
        user_id = user_data.get('id', 'N/A')
        country = user_data.get('country', 'N/A')
        product = user_data.get('product', 'N/A')

        # Affichage des informations extraites
        print(f"Display Name: {display_name}")
        print(f"External URL: {external_urls}")
        print(f"User ID: {user_id}")
        print(f"Country: {country}")
        print(f"Product: {product}")

    return user_data

# 4. Récupération des musiques récemment écoutées
def get_recent_tracks(access_token):
    tracks_url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    params = {
        'limit': 10
    }

    response = requests.get(tracks_url, headers=headers, params=params)

    # Vérifier le statut HTTP
    if response.status_code == 200:
        get_recent_tracks = response.json()
        return get_recent_tracks['items'] if 'items' in get_recent_tracks else None
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None


if __name__ == '__main__':
    auth_code = get_authorization_code()  # 1.
    access_token = get_access_token(auth_code)  # 2.
    
    if access_token:
        user_data = get_user_data(access_token)  # 3.

        recent_tracks = get_recent_tracks(access_token) # 4.
        if recent_tracks:
            print("Musiques récemment écoutées :")

            # Init listes
            track_names = []
            artist_names = []
            played_ats = []

            for track in recent_tracks:
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                played_at = track['played_at']
                
                # Ajout des data aux listes
                track_names.append(track_name)
                artist_names.append(artist_name)
                played_ats.append(played_at)
            
            # Création du df à partir des listes
            track_dict = {
                "track": track_names,
                "artist": artist_names,
                "played_at": played_ats
            }

            track_df = pd.DataFrame(track_dict, columns=["track", "artist", "played_at"])
            # add timestamps
            track_df['timestamps'] = pd.to_datetime(track_df['played_at']).dt.strftime('%Y-%m-%d')
            if check_data(track_df):
                print(track_df)
                print("Data validée")
        
# Load

engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect('my_played_tracks.sqlite')
cursor = conn.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS my_played_tracks(
    track VARCHAR(200),
    artist VARCHAR(200),
    played_at VARCHAR(200),
    timestamps VARCHAR(200),
    CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
)
"""

cursor.execute(sql_query)
print("Database créée")

try:
    track_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
except:
    print("Data déjà existante dans la database")

conn.close()
print("Fermeture de la base effectuée")