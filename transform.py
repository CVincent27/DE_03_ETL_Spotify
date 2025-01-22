import pandas as pd

def filter_recent_tracks(track_df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtre les musiques écoutées dans les dernières 24 heures.
    """
    # Récupérer le timestamp actuel moins 24h, en UTC
    last_24h = pd.Timestamp.now(tz='UTC') - pd.Timedelta(hours=24)
    
    # Convertir last_24h en datetime64[ns] sans fuseau horaire
    last_24h = last_24h.tz_localize(None)

    # Localiser les timestamps en UTC si tz-naive
    track_df['played_at'] = pd.to_datetime(track_df['played_at'])

    # Vérifier si les timestamps sont tz-naive et les localiser en UTC si nécessaire
    if track_df['played_at'].dt.tz is None:
        track_df['played_at'] = track_df['played_at'].dt.tz_localize('UTC')
    else:
        track_df['played_at'] = track_df['played_at'].dt.tz_convert('UTC')

    # Supprimer le fuseau horaire pour obtenir le format sans +00:00
    track_df['played_at'] = track_df['played_at'].dt.tz_localize(None)

    # Filtrer les lignes dont les timestamps sont dans les 24 dernières heures
    filtered_df = track_df[track_df['played_at'] > last_24h]

    return filtered_df
