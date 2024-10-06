
import pandas as pd


def transform_pbp_raw_to_play_player(pbp_raw: pd.DataFrame) -> pd.DataFrame:
    pdp = pbp_raw.copy()

    common_cols = [
        ('down', 'down'),
        ('game_id', 'game_id'),
        ('play_id', 'play_id'),
        ('play_type', 'play_type'),
        ('season', 'season'),
        ('season_type', 'season_type'),
        ('week', 'week'),
        ('pos_team', 'posteam')
    ]

    pass_cols = [
        ('player_id', 'passer_player_id'),
        ('player_name', 'passer_player_name'),
        ('pass_attempts', 'pass_attempt'),
        ('pass_completes', 'complete_pass'),
        ('pass_yards', 'passing_yards'),
        ('air_yards', 'air_yards'),
        ('pass_tds', 'pass_touchdown'),
        ('pass_int', 'interception'),
        ('pass_fumb_lost', lambda x: x["fumble"] if x["passer_player_id"]
            == x["fumbled_1_player_id"] else 0),
        ('pass_2pt', lambda x: 1 if x['two_point_conv_result'] == 'success'
            else 0)
    ]

    rush_cols = [
        ('player_id', 'rusher_player_id'),
        ('player_name', 'rusher_player_name'),
        ('rush_attempts', 'rush_attempt'),
        ('rush_yards', 'rushing_yards'),
        ('rush_tds', 'rush_touchdown'),
        ('rush_fumb_lost', lambda x: x["fumble"] if x["rusher_player_id"]
            == x["fumbled_1_player_id"] else 0),
        ('rush_2pt', lambda x: 1 if x['two_point_conv_result'] == 'success'
            else 0)
    ]

    rec_cols = [
        ('player_id', 'receiver_player_id'),
        ('player_name', 'receiver_player_name'),
        ('rec_targets', 'pass_attempt'),
        ('rec_receptions', 'complete_pass'),
        ('rec_yards', 'receiving_yards'),
        ('rec_tds', 'pass_touchdown'),
        ('rec_fumb_lost', lambda x: x["fumble"] if x["receiver_player_id"]
            == x["fumbled_1_player_id"] else 0),
        ('rec_2pt', lambda x: 1 if x['two_point_conv_result'] == 'success'
            else 0)
    ]

    def transform_columns(df, cols):
        """
        Transforms raw play-by-play data to play player data.
        Args:
            df (pandas.DataFrame): The raw play-by-play data.
            cols (list): A list of dictionaries representing the columns
                to be transformed.
        Returns:
            pandas.DataFrame: The transformed play player data.
        """
        new_df = pd.DataFrame()
        df = df.copy()
        for target, source in cols:
            if callable(source):
                new_df[target] = df.apply(source, axis=1)
            else:
                new_df[target] = df[source]
        return new_df

    pbp_pass_df_raw = pdp[pdp['play_type'] == 'pass']
    pbp_rec_df_raw = pbp_pass_df_raw.copy()
    pbp_rush_df_raw = pdp[pdp['play_type'] == 'run']

    pbp_pass_df_transformed = transform_columns(
        pbp_pass_df_raw, pass_cols + common_cols)
    pbp_rush_df_transformed = transform_columns(
        pbp_rush_df_raw, rush_cols + common_cols)
    pbp_rec_df_transformed = transform_columns(
        pbp_rec_df_raw, rec_cols + common_cols)

    play_player_stg = pd.concat([
        pbp_pass_df_transformed,
        pbp_rush_df_transformed,
        pbp_rec_df_transformed])

    return play_player_stg.copy()
