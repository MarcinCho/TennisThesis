import pandas as pd

time_interval_player_vs_player = pd.Timedelta(days=730)

# time_window = pd.Timedelta(days=730)


def avgOpponentStats(database, name, date, opprank, match_id):
    # Creats features from previous matches for match that will be played

    w_df = database.loc[(database['date'] > (
        date - time_interval_player_vs_player)) & (database['date'] < date) & ((database['P1_name'] == name) & (database['P2_Glicko'] > opprank - 100) & (database['P2_Glicko'] < opprank + 100))]

    l_df = database.loc[(database['date'] > (
        date - time_interval_player_vs_player)) & (database['date'] < date) & ((database['P2_name'] == name) & (database['P1_Glicko'] > opprank - 100) & (database['P1_Glicko'] < opprank + 100))]

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
