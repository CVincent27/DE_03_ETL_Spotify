import requests
import base64
import json
import os

# Infos de l'application
CLIENT_ID = '5e3fcd8ba2f046d9862f645e4a620eda'
CLIENT_SECRET = '003729ad92684faa994340f14b190f7c'
REDIRECT_URI = 'http://127.0.0.1:5500/'
SCOPE = 'user-read-private user-read-email'

# 1. Obtenir le code d'autorisation
def get_authorization_code():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    print(f"Code d'authentification : {auth_url}")
    
    auth_code = input("Entrez le code : ")
    return auth_code

# 2. échanger le code contre le token
def get_access_token(auth_code):
    token_url = "https://accounts.spotify.com/api/token"
    
if __name__ == '__main__':
    auth_code = get_authorization_code()  # Étape 1
    access_token = get_access_token(auth_code)  # Étape 2
    
