import pandas as pd

time_int = pd.Timedelta(days=730)


def pvpStats(db, match, player=1):
    date = match['date']
    surface = match['surface']
    name = match['P1_name'] if player == 1 else match['P2_name']
    name2 = match['P2_name'] if player == 1 else match['P1_name']
    rank1 = match['P1_rank'] if player == 1 else match['P2_rank']
    rank2 = match['P2_rank'] if player == 1 else match['P1_rank']
    match_id = match['match_id']

    w_df = db.loc[(db['date'] > (
        date - time_int)) & (db['date'] < date) & ((db['P1_name'] == name) & (db['P2_name'] == name2))]

    l_df = db.loc[(db['date'] > (
        date - time_int)) & (db['date'] < date) & ((db['P2_name'] == name) & (db['P1_name'] == name2))]

    if w_df.empty and l_df.empty:
        print('pvp empty')
        features = common_opponent_features(db, match, name, name2)
        if features is None:
            print('co empty')
            rank = rank2 if player == 1 else rank1
            features = avgOpponent(db, name, date, rank, match_id)
            if features is None:
                print('avg empty')
                return None

    surface_win = w_df.loc[w_df['surface'] == surface]
    surface_lose = l_df.loc[l_df['surface'] == surface]

    win_percentage = w_df.shape[0] / (w_df.shape[0] + l_df.shape[0]) if (
        w_df.shape[0] + l_df.shape[0]) != 0 else 0

    surface_win_percentage = surface_win.shape[0] / (surface_win.shape[0] + surface_lose.shape[0]) if (
        surface_win.shape[0] + surface_lose.shape[0]) != 0 else 0

    aceDf = (w_df['w_ace'].mean() + l_df['l_ace'].mean()) / (w_df['w_df'].mean() +
                                                             l_df['l_df'].mean()) if (w_df['w_df'].mean() + l_df['l_df'].mean()) != 0 else 0

    bp_factor = ((w_df['w_bpSaved'].mean() + l_df['l_bpSaved'].mean())) + (l_df['l_bpFaced'].mean() +
                                                                           w_df['w_bpFaced'].mean()) if (w_df['w_bpFaced'].mean() + l_df['l_bpFaced'].mean()) != 0 else 0

    points_on_return = (w_df['l_svpt'].mean() - (w_df['l_1stWon'].mean() + w_df['l_2ndWon'].mean())) + (
        l_df['w_svpt'].mean() - (l_df['w_1stWon'].mean() + l_df['w_2ndWon'].mean()))

    ace_probability = (w_df['w_ace'].mean() + l_df['l_ace'].mean()) / (w_df['w_svpt'].mean(
    ) + l_df['l_svpt'].mean()) if (w_df['w_svpt'].mean() + l_df['l_svpt'].mean()) != 0 else 0

    first_serve_return = w_df['l_1stIn'].mean(
    ) - w_df['l_1stWon'].mean() + l_df['w_1stIn'].mean() - l_df['w_1stWon'].mean()

    features = pd.DataFrame({
        'match_id': match_id,
        'win_percentage': win_percentage,
        'surface_win_percentage': surface_win_percentage,
        'aceDF': aceDf,
        'bp_factor': bp_factor,
        'points_on_return': points_on_return,
        'ace_probability': ace_probability,
        'first_serve_return': first_serve_return,

    }, index=[0]
    )

    return features


def common_opponent(db, player1, player2, date):
    # Returns list of common opponents between two players
    player1_df = db.loc[(db['date'] > (
        date - time_int)) & (db['date'] < date) & ((db['P1_name'] == player1) | (db['P2_name'] == player1))]

    player2_df = db.loc[(db['date'] > (
        date - time_int)) & (db['date'] < date) & ((db['P1_name'] == player2) | (db['P2_name'] == player2))]

    player1_opponents = player1_df['P1_name'].unique().tolist() + \
        player1_df['P2_name'].unique().tolist()
    player2_opponents = player2_df['P1_name'].unique().tolist() + \
        player2_df['P2_name'].unique().tolist()

    common_opponents = list(set(player1_opponents) & set(player2_opponents))

    if len(common_opponents) == 0:
        return None

    return common_opponents


def common_opponent_features(db, match, name1, name2):
    player1 = name1
    player2 = name2

    date = match['date']
    opponents = common_opponent(db, player1, player2, date)

    if opponents is None:
        return None

    else:
        player_CO_features = pd.DataFrame()
        for opponent in opponents:
            player_CO_features = commonOpponent(
                db, player1, date, opponent, match['match_id'])

    return player_CO_features


def commonOpponent(db, name, date, name2, match_id):
    # Creats features from previous matches for match that will be played

    w_df = db.loc[(db['date'] > (
        date - time_int
    )) & (db['date'] < date) & ((db['P1_name'] == name) & (db['P2_name'] == name2))]

    l_df = db.loc[(db['date'] > (
        date - time_int
    )) & (db['date'] < date) & ((db['P2_name'] == name) & (db['P1_name'] == name2))]

    games_played = w_df.shape[0] + l_df.shape[0]
    # random starts
    win_percentage = w_df.shape[0] / games_played if games_played != 0 else 0

    first_won_serve = ((w_df['w_1stWon'].mean() / w_df['w_svpt'].mean()) + (l_df['l_1stWon'].mean(
    ) / l_df['l_svpt'].mean())) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    second_won_serve = ((w_df['w_2ndWon'].mean() / w_df['w_svpt'].mean()) + (l_df['l_2ndWon'].mean(
    ) / l_df['l_svpt'].mean())) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    points_on_return = (w_df['l_svpt'].mean() - (w_df['l_1stWon'].mean() + w_df['l_2ndWon'].mean())) + (
        l_df['w_svpt'].mean() - (l_df['w_1stWon'].mean() + l_df['w_2ndWon'].mean()))

    serve_points_won = (second_won_serve + first_won_serve) / (w_df['w_svpt'].mean(
    ) + l_df['l_svpt'].mean()) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    ace_probability = w_df['w_ace'].mean() / w_df['w_svpt'].mean() + \
        l_df['l_ace'].mean() / \
        l_df['l_svpt'].mean() if w_df['w_svpt'].mean() != 0 else 0

    df_probability = w_df['w_df'].mean() / w_df['w_svpt'].mean() + \
        l_df['l_df'].mean() / \
        l_df['l_svpt'].mean() if w_df['w_svpt'].mean() != 0 else 0

    first_serve_return = w_df['l_1stIn'].mean(
    ) - w_df['l_1stWon'].mean() + l_df['w_1stIn'].mean() - l_df['w_1stWon'].mean()

    features = pd.DataFrame({
        'match_id': match_id,
        'win_percentage': win_percentage,
        'first_won_serve': first_won_serve,
        'second_won_serve': second_won_serve,
        'points_on_return': points_on_return,
        'serve_points_won': serve_points_won,
        'ace_probability': ace_probability,
        'df_probability': df_probability,
        'first_serve_return': first_serve_return,


    }, index=[0]
    )

    return features


def avgOpponent(db, name, date, rank, match_id):
    # Creats features from previous matches for match that will be played

    w_df = db.loc[(db['date'] > (
        date - time_int
    )) & (db['date'] < date) & ((db['P1_name'] == name) & (db['P2_rank'] > rank - 10) & (db['P2_rank'] < rank + 50))]

    l_df = db.loc[(db['date'] > (
        date - time_int
    )) & (db['date'] < date) & ((db['P2_name'] == name) & (db['P1_rank'] > rank - 50))]

    if w_df.empty and l_df.empty:
        return None

    games_played = w_df.shape[0] + l_df.shape[0]
    # random starts
    win_percentage = w_df.shape[0] / games_played if games_played != 0 else 0

    first_won_serve = ((w_df['w_1stWon'].mean() / w_df['w_svpt'].mean()) + (l_df['l_1stWon'].mean(
    ) / l_df['l_svpt'].mean())) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    second_won_serve = ((w_df['w_2ndWon'].mean() / w_df['w_svpt'].mean()) + (l_df['l_2ndWon'].mean(
    ) / l_df['l_svpt'].mean())) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    points_on_return = (w_df['l_svpt'].mean() - (w_df['l_1stWon'].mean() + w_df['l_2ndWon'].mean())) + (
        l_df['w_svpt'].mean() - (l_df['w_1stWon'].mean() + l_df['w_2ndWon'].mean()))

    serve_points_won = (second_won_serve + first_won_serve) / (w_df['w_svpt'].mean(
    ) + l_df['l_svpt'].mean()) if w_df['w_svpt'].mean() and l_df['l_svpt'].mean() != 0 else 0

    ace_probability = w_df['w_ace'].mean() / w_df['w_svpt'].mean() + \
        l_df['l_ace'].mean() / \
        l_df['l_svpt'].mean() if w_df['w_svpt'].mean() != 0 else 0

    df_probability = w_df['w_df'].mean() / w_df['w_svpt'].mean() + \
        l_df['l_df'].mean() / \
        l_df['l_svpt'].mean() if w_df['w_svpt'].mean() != 0 else 0

    first_serve_return = w_df['l_1stIn'].mean(
    ) - w_df['l_1stWon'].mean() + l_df['w_1stIn'].mean() - l_df['w_1stWon'].mean()

    features = pd.DataFrame({
        'match_id': match_id,
        'win_percentage': win_percentage,
        'first_won_serve': first_won_serve,
        'second_won_serve': second_won_serve,
        'points_on_return': points_on_return,
        'serve_points_won': serve_points_won,
        'ace_probability': ace_probability,
        'df_probability': df_probability,
        'first_serve_return': first_serve_return,


    }, index=[0]
    )

    return features
