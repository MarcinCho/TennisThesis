import pandas as pd


def openFiles(where):

    db = pd.read_csv(where)
    db["date"] = pd.to_datetime(db["date"], format="%Y%m%d").dt.date

    return db


time_interval_current_form = pd.Timedelta(days=183)
time_interval_player_vs_player = pd.Timedelta(days=730)


def createFeatures(database, name, date, rank):
    win_database = database.loc[
        (database["date"] > (date - time_interval_player_vs_player))
        & (database["date"] < date)
        & (database["P1_name"] == name)
    ]

    lose_database = database.loc[
        (database["date"] > (date - time_interval_player_vs_player))
        & (database["date"] < date)
        & (database["P2_name"] == name)
    ]

    print(win_database.shape)
    print(lose_database.shape)

    features = pd.DataFrame(
        {
            "date": date,  # has to be here for merge to work
            "name": name,
            "rank_points": rank,
            "height": win_database["P1_ht"].mean(),
            "age": win_database["P1_age"].mean(),
            "wins": win_database.shape[0],
            "loses": lose_database.shape[0],
            "matches_played": win_database.shape[0] + lose_database.shape[0],
            "win_percentage": (
                win_database.shape[0] / (win_database.shape[0] + lose_database.shape[0])
                if (win_database.shape[0] + lose_database.shape[0]) != 0
                else 0
            ),
            "w_ace": win_database["w_ace"].mean(),
            "w_df": win_database["w_df"].mean(),
            "w_svpt": win_database["w_svpt"].mean(),
            "w_1stIn": win_database["w_1stIn"].mean(),
            "w_1stWon": win_database["w_1stWon"].mean(),
            "w_2ndWon": win_database["w_2ndWon"].mean(),
        },
        index=[0],
    )

    return features


def matchInfo(database, name1, name2, date):

    match_info = pd.DataFrame(
        {
            "date": date,
            "surface": database.loc[
                (database["date"] == date)
                & ((database["P1_name"] == name1) | (database["P2_name"] == name2))
            ]["surface"].mode()[0],
            "tourney_level": database.loc[
                (database["date"] == date)
                & ((database["P1_name"] == name1) | (database["P2_name"] == name2))
            ]["level"].mode()[0],
            "who_won": 1,
        }
    )

    return match_info
