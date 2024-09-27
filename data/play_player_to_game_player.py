def transform_play_player_to_game_player(play_player_df):
    # GAME LEVEL AGGREGATION
    game_player = play_player_df.groupby(['game_id', 'player_id']).agg({
        'display_name': 'first',
        'position': 'first',
        'birth_date': 'first',
        'season': 'first',
        'season_type': 'first',
        'week': 'first',
        'pos_team': 'first',
        'player_name': 'first',
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
        'fp': 'sum'
    }).reset_index()

    game_player['target_share'] = game_player['rec_targets'] / \
        game_player.groupby(['game_id', 'pos_team'])[
        'rec_targets'].transform('sum')

    game_player['rush_share'] = game_player['rush_attempts'] / \
        game_player.groupby(['game_id', 'pos_team'])[
        'rush_attempts'].transform('sum')

    game_player['pass_share'] = game_player['pass_attempts'] / \
        game_player.groupby(['game_id', 'pos_team'])[
        'pass_attempts'].transform('sum')
    
    game_player['rank'] = game_player.groupby(
        'week')['fp'].rank(ascending=False)

    game_player['pos_rank'] = game_player.groupby([
        'week', 'position'])['fp'].rank(ascending=False)

    return game_player
