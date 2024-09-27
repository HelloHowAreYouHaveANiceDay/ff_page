
import json

import pandas as pd
from data import play_player_to_game_player
from data.fantasy import calculate_fantasy_points
from data.pbp_raw_to_play_player import transform_pbp_raw_to_play_player
from data.player import merge_player_metadata


fantasy_config = json.load(open('fantasy_config.json'))
player_df = pd.read_parquet('./raw/players/players.parquet')


def raw_to_pp(raw):
    play_player = transform_pbp_raw_to_play_player(raw)
    play_player_fantasy = calculate_fantasy_points(fantasy_config, play_player)
    play_player_fantasy_merged = merge_player_metadata(play_player_fantasy,
                                                       player_df)
    return play_player_fantasy_merged


def pp_to_gp(play_player):
    return play_player_to_game_player(play_player)


