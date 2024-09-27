
import pandas as pd


def merge_player_metadata(play_player: pd.DataFrame, players: pd.DataFrame):
    pp = play_player.copy()

    pp = pd.merge(pp, players[[
        'gsis_id', 'display_name', 'position', 'birth_date']],
        left_on='player_id', right_on="gsis_id", how='left')

    return pp.copy()
