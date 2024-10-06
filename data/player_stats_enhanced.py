

from fantasy import (
    calculate_game_fantasy_points,
    calculate_pass_points,
    calculate_rec_points,
    calculate_rush_points
)


def game_player_stats(player_stats, fantasy_config):
    # stats reference:
    # https://www.nflfastr.com/reference/calculate_player_stats.html

    # rename columns
    player_stats.rename(columns={
        'recent_team': 'pos_team',
        'completions': 'pass_completions',
        'attempts': 'pass_attempts',
        'passing_yards': 'pass_yards',
        'passing_tds': 'pass_tds',
        'interceptions': 'pass_int',
        'sack_fumbles_lost': 'pass_fumb_lost',
        'passing_air_yards': 'pass_air_yards',
        'passing_yards_after_catch': 'pass_yards_after_catch',
        'passing_first_downs': 'pass_first_downs',
        'passing_epa': 'pass_epa',
        'passing_2pt_conversions': 'pass_2pt',
        'pacr': 'pass_air_conv_ratio',
        'rushing_yards': 'rush_yards',
        'rushing_tds': 'rush_tds',
        'rushing_fumbles': 'rush_fumbles',
        'rushing_fumbles_lost': 'rush_fumb_lost',
        'rushing_first_downs': 'rush_first_downs',
        'rushing_epa': 'rush_epa',
        'rushing_2pt_conversions': 'rush_2pt',
        'receptions': 'rec_receptions',
        'targets': 'rec_targets',
        'receiving_yards': 'rec_yards',
        'receiving_tds': 'rec_tds',
        'receiving_fumbles': 'rec_fumbles',
        'receiving_fumbles_lost': 'rec_fumb_lost',
        'receiving_air_yards': 'rec_air_yards',
        'receiving_yards_after_catch': 'rec_yards_after_catch',
        'receiving_first_downs': 'rec_first_downs',
        'receiving_epa': 'rec_epa',
        'receiving_2pt_conversions': 'rec_2pt',
        'racr': 'rec_air_conv_ratio',
        'target_share': 'rec_target_share',
        'air_yards_share': 'rec_air_yards_share',
        'wopr': 'rec_weighted_opp_rating'
    }, inplace=True)

    player_stats = calculate_game_fantasy_points(fantasy_config, player_stats)

    player_stats['rush_share'] = player_stats['carries'] / \
        player_stats.groupby(['week', 'pos_team'])[
        'carries'].transform('sum')

    player_stats['pass_share'] = player_stats['pass_attempts'] / \
        player_stats.groupby(['week', 'pos_team'])[
        'pass_attempts'].transform('sum')

    player_stats['rank'] = player_stats.groupby(
        'week')['fp'].rank(ascending=False)

    player_stats['pos_rank'] = player_stats.groupby([
        'week', 'position'])['fp'].rank(ascending=False)

    return player_stats
