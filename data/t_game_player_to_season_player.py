import pandas as pd


def transform_game_player_to_season_player(game_player_df):

    season_player = game_player_df.groupby(['season', 'player_id']).agg({
        'player_name': 'first',
        'position': 'first',
        'birth_date': 'first',
        'display_name': 'first',
        'game_id': 'nunique',
        'pass_attempts': 'sum',
        'pass_completes': 'sum',
        'pass_yards': 'sum',
        'air_yards': 'sum',
        'pass_tds': 'sum',
        'pass_int': 'sum',
        'pass_2pt': 'sum',
        'pass_fp': 'sum',
        'rush_attempts': 'sum',
        'rush_yards': 'sum',
        'rush_tds': 'sum',
        'rush_2pt': 'sum',
        'rush_fp': 'sum',
        'rec_targets': 'sum',
        'rec_completes': 'sum',
        'rec_yards': 'sum',
        'rec_tds': 'sum',
        'rec_2pt': 'sum',
        'rec_fp': 'sum',
        'fp': 'sum',
        'target_share': 'mean',
        'rush_share': 'mean',
        'pass_share': 'mean'
    }).rename(columns={
        'game_id': 'games',
        'target_share': 'avg_target_share',
        'rush_share': 'avg_rush_share',
        'pass_share': 'avg_pass_share'
    })

    # Gamelists track values for each game in a season.
    # Used for visualization
    #
    # Create a full range of game IDs for each season and player
    full_game_ids = game_player_df.set_index([
        'season', 'player_id', 'week']).unstack(fill_value=None).stack(
            future_stack=True).reset_index()
    # Reindex the DataFrame to include all game IDs, filling missing values
    # with None
    game_player_df_reindexed = game_player_df.set_index(
        ['season', 'player_id', 'game_id']).reindex(
        full_game_ids.set_index(['season', 'player_id', 'game_id']).index,
        fill_value=None).reset_index()
    # Group by season and player_id, then apply the list function
    fp_glist = game_player_df_reindexed.groupby(
        ['season', 'player_id'])['fp'].apply(list).reset_index()
    target_share_glist = game_player_df_reindexed.groupby(
        ['season', 'player_id'])['target_share'].apply(list).reset_index()
    rush_share_glist = game_player_df_reindexed.groupby(
        ['season', 'player_id'])['rush_share'].apply(list).reset_index()
    pass_share_glist = game_player_df_reindexed.groupby(
        ['season', 'player_id'])['pass_share'].apply(list).reset_index()

    a = pd.merge(season_player, fp_glist, on=[
        'season', 'player_id'], how='left').rename(columns={
            'fp_x': 'fp',
            'fp_y': 'fp_glist'
        })
    b = pd.merge(a, target_share_glist, on=[
        'season', 'player_id'], how='left').rename(columns={
            'target_share': 'target_share_glist'
        })
    c = pd.merge(b, rush_share_glist, on=[
        'season', 'player_id'], how='left').rename(columns={
            'rush_share': 'rush_share_glist'
        })
    d = pd.merge(c, pass_share_glist, on=[
        'season', 'player_id'], how='left').rename(columns={
            'pass_share': 'pass_share_glist'
        })
    season_player = d

    season_player['rank'] = season_player.groupby(
        'season')['fp'].rank(ascending=False)

    season_player['pos_rank'] = season_player.groupby(
        'position')['fp'].rank(ascending=False)

    return season_player
