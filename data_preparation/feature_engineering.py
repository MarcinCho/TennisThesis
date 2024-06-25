import pandas as pd


def openFiles(where):

    db = pd.read_csv(where)
    db['date'] = pd.to_datetime(db['date'], format='%Y%m%d').dt.date

    return db


time_interval_current_form = pd.Timedelta(days=183)
time_interval_player_vs_player = pd.Timedelta(days=730)


def createFeatures(database, name, date, rank):
    # Creats features from previous matches for match that will be played

    win_database = database.loc[(database['date'] > (
        date - time_interval_player_vs_player)) & (database['date'] < date) & (database['P1_name'] == name)]

    lose_database = database.loc[(database['date'] > (
        date - time_interval_player_vs_player)) & (database['date'] < date) & (database['P2_name'] == name)]

    print(win_database.shape)
    print(lose_database.shape)

    features = pd.DataFrame({
        'date': date,  # has to be here for merge to work
        'name': name,
        'rank_points': rank,
        # 'hand': win_database['P1_hand'][0],
        'height': win_database['P1_ht'].mean(),
        'age': win_database['P1_age'].mean(),  # just for now
        'wins': win_database.shape[0],
        'loses': lose_database.shape[0],
        'matches_played': win_database.shape[0] + lose_database.shape[0],
        'win_percentage': win_database.shape[0] / (win_database.shape[0] + lose_database.shape[0]) if (win_database.shape[0] + lose_database.shape[0]) != 0 else 0,
        'w_ace': win_database['w_ace'].mean(),
        'w_df': win_database['w_df'].mean(),
        'w_svpt': win_database['w_svpt'].mean(),
        'w_1stIn': win_database['w_1stIn'].mean(),
        'w_1stWon': win_database['w_1stWon'].mean(),
        'w_2ndWon': win_database['w_2ndWon'].mean(),
        # 'w_SvGms': win_database['w_SvGms'].mean(),
        # 'w_bpSaved': win_database['w_bpSaved'].mean(),
        # 'w_bpFaced': win_database['w_bpFaced'].mean(),
        # 'l_ace': lose_database['l_ace'].mean(),
        # 'l_df': lose_database['l_df'].mean(),
        # 'l_svpt': lose_database['l_svpt'].mean(),
        # 'l_1stIn': lose_database['l_1stIn'].mean(),
        # 'l_1stWon': lose_database['l_1stWon'].mean(),
        # 'l_2ndWon': lose_database['l_2ndWon'].mean(),
        # 'l_SvGms': lose_database['l_SvGms'].mean(),
        # 'l_bpSaved': lose_database['l_bpSaved'].mean(),
        # 'l_bpFaced': lose_database['l_bpFaced'].mean(),
        # 'w_ace%': win_database['w_ace'].mean() / win_database['w_svpt'].mean() if win_database['w_svpt'].mean() != 0 else 0,
        # 'w_df%': win_database['w_df'].mean() / win_database['w_svpt'].mean() if win_database['w_svpt'].mean() != 0 else 0,
        # 'l_ace%': lose_database['l_ace'].mean() / lose_database['l_svpt'].mean() if lose_database['l_svpt'].mean() != 0 else 0,
        # 'l_df%': lose_database['l_df'].mean() / lose_database['l_svpt'].mean() if lose_database['l_svpt'].mean() != 0 else 0,

    }, index=[0]
    )

    return features


def matchInfo(database, name1, name2, date):
    # Saves basic info about match date, surface, tourney_level, and who won

    match_info = pd.DataFrame({
        'date': date,
        'surface': database.loc[(database['date'] == date) & ((database['P1_name'] == name1) | (database['P2_name'] == name2))]['surface'].mode()[0],
        'tourney_level': database.loc[(database['date'] == date) & ((database['P1_name'] == name1) | (database['P2_name'] == name2))]['level'].mode()[0],
        'who_won': 1
    })

    return match_info
