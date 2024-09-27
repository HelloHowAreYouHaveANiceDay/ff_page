
import json
import os
import pandas as pd
from play_player_to_game_player import transform_play_player_to_game_player
from fantasy import calculate_fantasy_points
from pbp_raw_to_play_player import transform_pbp_raw_to_play_player
from player import merge_player_metadata
from raw_fetch import download_play_by_play, download_players

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the full path to the JSON file
fc_path = os.path.join(script_dir, 'fantasy_config.json')

fantasy_config = json.load(open(fc_path))


def script_path(relative_path):
    return os.path.join(script_dir, relative_path)


def raw_to_pp(raw):
    player_df = pd.read_parquet(script_path('./raw/players/players.parquet'))
    play_player = transform_pbp_raw_to_play_player(raw)
    play_player_fantasy = calculate_fantasy_points(fantasy_config, play_player)
    play_player_fantasy_merged = merge_player_metadata(play_player_fantasy,
                                                       player_df)
    return play_player_fantasy_merged


def pp_to_gp(play_player):
    return transform_play_player_to_game_player(play_player)


def update_2024():
    download_play_by_play(2024)
    download_players()

    pbp = pd.read_parquet(script_path('./raw/pbp/play_by_play_2024.parquet'))

    play_player = raw_to_pp(pbp)
    game_player = pp_to_gp(play_player)

    # save to frontend
    play_player.to_parquet(script_path(
        '../src/data/play_player_2024.parquet'), index=False)
    game_player.to_parquet(script_path(
        '../src/data/game_player_2024.parquet'), index=False)
