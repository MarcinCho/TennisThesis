import pandas as pd

time_int = pd.Timedelta(days=7300)


def pvpStats(database, match, player=1):
    date = match['date']
    surface = match['surface']
    name = match['P1_name'] if player == 1 else match['P2_name']
    name2 = match['P2_name'] if player == 1 else match['P1_name']
    match_id = match['match_id']

    w_df = database.loc[(database['date'] > (
        date - time_int)) & (database['date'] < date) & ((database['P1_name'] == name) & (database['P2_name'] == name2))]

    l_df = database.loc[(database['date'] > (
        date - time_int)) & (database['date'] < date) & ((database['P2_name'] == name) & (database['P1_name'] == name2))]

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

    if w_df.empty or l_df.empty:
        return pd.DataFrame({
            'match_id': match_id,
            'win_percentage': 0.5,
            'surface_win_percentage': 0.5,
            'aceDF': 0.5,
            'bp_factor': 0.5,
            'points_on_return': 0.5,
            'ace_probability': 0.5,
            'first_serve_return': 0.5,
        }, index=[0])

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
