import os
import requests


PARQUET = 'parquet'

DATA_DIR = os.path.join(os.path.dirname(__file__), 'raw')


def play_by_play_url(season):
    url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/"\
        f"play_by_play_{season}.{PARQUET}"
    return url


def player_url():
    url = "https://github.com/nflverse/nflverse-data/releases/download/"\
        f"players/players.{PARQUET}"
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
    url = play_by_play_url(season)
    filename = os.path.join(
        DATA_DIR, 'pbp', f'play_by_play_{season}.{PARQUET}')
    download_file(url, filename)


def download_players():
    """
    Downloads the player data.
    """
    url = player_url()
    filename = os.path.join(DATA_DIR, 'players', f'players.{PARQUET}')
    download_file(url, filename)


def download_all_seasons():
    """
    Downloads the play-by-play data for all seasons.
    """
    for season in range(2019, 2024):
        download_play_by_play(season)
