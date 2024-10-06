
import json
import os
import pandas as pd
from player_stats_enhanced import game_player_stats
from play_player_to_game_player import transform_play_player_to_game_player
from fantasy import calculate_fantasy_points
from pbp_raw_to_play_player import transform_pbp_raw_to_play_player
from player import merge_player_metadata
from raw_fetch import (
    download_play_by_play,
    download_players,
    download_weekly_player_stats
    )

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


def join_gp_to_game_stats(game_player, game_stats):
    # join on week, player_id
    return game_player.merge(game_stats, on=['week', 'player_id'])


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


def update_game_player_2024():
    download_weekly_player_stats(2024)
    download_players()

    game_stats = pd.read_parquet(
        script_path('./raw/player_stats/player_stats_2024.parquet')
    )

    game_player = game_player_stats(game_stats, fantasy_config)

    game_player.to_parquet(script_path(
        '../src/data/game_player_2024.parquet'), index=False)