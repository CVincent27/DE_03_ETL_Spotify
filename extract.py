import base64
import requests

CLIENT_ID = '02da1b0fd5474dc08cb4266d9dd13ae7'
CLIENT_SECRET = '5675b5ae4f664c339f81df5e7eca79b9'
REDIRECT_URI = 'http://127.0.0.1:5500/'
SCOPE = 'user-read-private%20user-read-email%20user-read-recently-played'

def get_authorization_code():
    """
    Récupère le code d'autorisation nécessaire pour obtenir le token d'accès.
    """
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    print(f"Code d'authentification : {auth_url}")
    auth_code = input("Entrez le code : ")
    return auth_code

def get_access_token(auth_code):
    """
    Échange le code d'autorisation contre un token d'accès.
    """
    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
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
        return None

def get_user_data(access_token):
    """
    Récupère les données de l'utilisateur Spotify.
    """
    user_url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erreur:", response.status_code)
        return None

def get_recent_tracks(access_token):
    """
    Récupère les musiques récemment écoutées de l'utilisateur.
    """
    tracks_url = "https://api.spotify.com/v1/me/player/recently-played"
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 10}
    response = requests.get(tracks_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['items']
    else:
        print(f"Erreur {response.status_code}: {response.text}")
        return None
