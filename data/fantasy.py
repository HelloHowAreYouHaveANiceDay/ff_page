

def calculate_pass_points(fantasy_config):
    def calculate_pass_points_with_config(row):
        points = 0
        points += row["pass_yards"] * fantasy_config["SCORING"]["PASS_YDS"]
        points += row["pass_tds"] * fantasy_config["SCORING"]["PASS_TD"]
        points += row["pass_int"] * fantasy_config["SCORING"]["INT"]
        points += row["pass_fumb_lost"] * fantasy_config["SCORING"]["FUM_LOST"]
        points += row["pass_2pt"] * fantasy_config["SCORING"]["PASS_2PT_CONV"]
        return points
    return calculate_pass_points_with_config


def calculate_rush_points(fantasy_config):
    def calculate_rush_points_with_config(row):
        points = 0
        points += row["rush_yards"] * fantasy_config["SCORING"]["RUSH_YDS"]
        points += row["rush_tds"] * fantasy_config["SCORING"]["RUSH_TD"]
        points += row["rush_fumb_lost"] * fantasy_config["SCORING"]["FUM_LOST"]
        points += row["rush_2pt"] * fantasy_config["SCORING"]["RUSH_2PT_CONV"]
        return points
    return calculate_rush_points_with_config


def calculate_rec_points(fantasy_config):
    def calculate_rec_points_with_config(row):
        points = 0
        points += row["rec_yards"] * fantasy_config["SCORING"]["REC_YDS"]
        points += row["rec_completes"] * fantasy_config["SCORING"]["REC_EACH"]
        points += row["rec_tds"] * fantasy_config["SCORING"]["REC_TD"]
        points += row["rec_fumb_lost"] * fantasy_config["SCORING"]["FUM_LOST"]
        points += row["rec_2pt"] * fantasy_config["SCORING"]["REC_2PT_CONV"]

        return points
    return calculate_rec_points_with_config


def calculate_fantasy_points(fantasy_config, play_player):
    pp = play_player.copy()

    pp["pass_fp"] = pp.apply(
        calculate_pass_points(fantasy_config), axis=1).fillna(0)
    pp["rush_fp"] = pp.apply(
        calculate_rush_points(fantasy_config), axis=1).fillna(0)
    pp["rec_fp"] = pp.apply(
        calculate_rec_points(fantasy_config), axis=1).fillna(0)
    
    pp["fp"] = pp["pass_fp"] + pp["rush_fp"] + pp["rec_fp"]

    return pp.copy()
