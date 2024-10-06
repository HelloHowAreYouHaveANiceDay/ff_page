import os
import requests


PARQUET = 'parquet'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'raw')

dl_url = "https://github.com/nflverse/nflverse-data/releases/download/"


def play_by_play_url(season):
    url = dl_url + f"pbp/play_by_play_{season}.{PARQUET}"
    return url


def player_stats_url(season):
    url = dl_url + f"player_stats/player_stats_{season}.{PARQUET}"
    return url


def snap_count_url(season):
    url = dl_url + f"snap_counts/snap_counts_{season}.{PARQUET}"
    return url


def player_url():
    url = dl_url + f"players/players.{PARQUET}"
    return url


def download_file(url, local_filename):
    """
    Downloads a file from the given URL and saves it locally.

    Parameters:
    url (str): The URL of the file to download.
    local_filename (str): The local path where the file will be saved.
    """
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception(f'Failed to download file: {response.status_code}')

    # Write the content to a local file
    with open(local_filename, 'wb') as file:
        file.write(response.content)

    return local_filename


def download_play_by_play(season):
    """
    Downloads the play-by-play data for the given season.

    Parameters:
    season (int): The season for which to download the data.
    """
    if not os.path.exists(os.path.join(DATA_DIR, 'pbp')):
        os.makedirs(os.path.join(DATA_DIR, 'pbp'), exist_ok=True)

    url = play_by_play_url(season)
    filename = os.path.join(
        DATA_DIR, 'pbp', f'play_by_play_{season}.{PARQUET}')
    download_file(url, filename)
    return filename


def download_snap_counts(season):
    """
    Downloads the snap count data for the given season.

    Parameters:
    season (int): The season for which to download the data.
    """
    # create snap_counts folder if doens't exist
    if not os.path.exists(os.path.join(DATA_DIR, 'snap_counts')):
        os.makedirs(os.path.join(DATA_DIR, 'snap_counts'), exist_ok=True)

    url = snap_count_url(season)
    filename = os.path.join(
        DATA_DIR, 'snap_counts', f'snap_counts_{season}.{PARQUET}')
    download_file(url, filename)
    return filename


def download_weekly_player_stats(season):
    """
    Downloads the player stats data for the given season.

    Parameters:
    season (int): The season for which to download the data.
    """
    if not os.path.exists(os.path.join(DATA_DIR, 'player_stats')):
        os.makedirs(os.path.join(DATA_DIR, 'player_stats'), exist_ok=True)

    url = player_stats_url(season)
    filename = os.path.join(
        DATA_DIR, 'player_stats', f'player_stats_{season}.{PARQUET}')
    download_file(url, filename)
    return filename


def download_players():
    """
    Downloads the player data.
    """
    if not os.path.exists(os.path.join(DATA_DIR, 'players')):
        os.makedirs(os.path.join(DATA_DIR, 'players'), exist_ok=True)

    url = player_url()
    filename = os.path.join(DATA_DIR, 'players', f'players.{PARQUET}')
    download_file(url, filename)


def download_pbp_all_seasons():
    """
    Downloads the play-by-play data for all seasons.
    """
    for season in range(2019, 2024):
        download_play_by_play(season)
