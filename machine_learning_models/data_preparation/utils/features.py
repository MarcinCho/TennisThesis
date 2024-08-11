import pandas as pd
import random
time_f = pd.Timedelta(
    days=180)  # equals one season same as rankings


def result_scrambler(database):

    db_with_wins = pd.DataFrame()

    for id, match in database.iterrows():
        date = match['tourney_date']
        sudo_random_number = random.randint(0, 100)

        p1 = pd.DataFrame({
            'match_id': match['match_id'],
            'name': match['winner_name'],
            'hand': match['winner_hand'],
            'entry': match['winner_entry'],
            'seed': match['winner_seed'],
            'age': match['winner_age'],
            'ht': match['winner_ht'],
            'ioc': match['winner_ioc'],
            'rank': match['winner_rank'],
            'rank_points': match['winner_rank_points'],
            'ace': match['w_ace'],
            'df': match['w_df'],
            'svpt': match['w_svpt'],
            '1stIn': match['w_1stIn'],
            '1stWon': match['w_1stWon'],
            '2ndWon': match['w_2ndWon'],
            'SvGms': match['w_SvGms'],
            'bpSaved': match['w_bpSaved'],
            'bpFaced': match['w_bpFaced']}, index=[0]) 

        p2 = pd.DataFrame({
            'match_id': match['match_id'],
            'name': match['loser_name'],
            'hand': match['loser_hand'],
            'entry': match['loser_entry'],
            'seed': match['loser_seed'],
            'age': match['loser_age'],
            'ht': match['loser_ht'],
            'ioc': match['loser_ioc'],
            'rank': match['loser_rank'],
            'rank_points': match['loser_rank_points'],
            'ace': match['l_ace'],
            'df': match['l_df'],
            'svpt': match['l_svpt'],
            '1stIn': match['l_1stIn'],
            '1stWon': match['l_1stWon'],
            '2ndWon': match['l_2ndWon'],
            'SvGms': match['l_SvGms'],
            'bpSaved': match['l_bpSaved'],
            'bpFaced': match['l_bpFaced']}, index=[0])

        if sudo_random_number % 2 == 0:
            # player 1 == winner y = 1
            match_vitals = pd.DataFrame({
                'match_id': match['match_id'],
                'date': date,
                'surface': match['surface'],
                'tourney_level': match['tourney_level'],
                'draw_size': match['draw_size'],
                'y': 1
            }, index=[0])
            player_stats_merged = pd.merge(
                p1, p2, on='match_id', suffixes=('_P1', '_P2'))
            player_stats_merged = pd.merge(
                match_vitals, player_stats_merged, on='match_id')
            db_with_wins = pd.concat(
                [player_stats_merged, db_with_wins], ignore_index=True)

        else:
            # player 2 == winner y = 0
            match_vitals = pd.DataFrame({
                'match_id': match['match_id'],
                'date': date,
                'surface': match['surface'],
                'tourney_level': match['tourney_level'],
                'draw_size': match['draw_size'],
                'y': 0
            }, index=[0])
            player_stats_merged = pd.merge(
                p2, p1, on='match_id', suffixes=('_P1', '_P2'))
            player_stats_merged = pd.merge(
                match_vitals, player_stats_merged, on='match_id')
            db_with_wins = pd.concat(
                [player_stats_merged, db_with_wins], ignore_index=True)

    return db_with_wins


def basicfeatureCreator(database):

    match_stats_with_features = pd.DataFrame()

    for id, match in database.iterrows():

        match_vitals = pd.DataFrame({
            'match_id': match['match_id'],
            'date': match['date'],
            'surface': match['surface'],
            'tourney_level': match['tourney_level'],
            'draw_size': match['draw_size'],
            'y': match['y']
        }, index=[0])

        player1_features = basicStats(
            database, match['name_P1'], match)
        player2_features = basicStats(
            database, match['name_P2'], match)
        player_stats_merged = pd.merge(
            player1_features, player2_features, on='match_id', suffixes=('_P1', '_P2'))
        player_stats_merged = pd.merge(
            match_vitals, player_stats_merged, on='match_id')

        match_stats_with_features = pd.concat(
            [player_stats_merged, match_stats_with_features], ignore_index=True)

    return match_stats_with_features


def basicStats(db, name, match):
    # Creats features from previous matches for match that will be played
    if name == match['name_P1']:
        rank_official = match['rank_P1']
        rank_points = match['rank_points_P1']
        rank_elo = match['elo_P1']
        rank_glicko = match['glicko_P1']
        hand = match['hand_P1']
        height = match['ht_P1']
    else:
        rank_official = match['rank_P2']
        rank_points = match['rank_points_P2']
        rank_elo = match['elo_P2']
        rank_glicko = match['glicko_P2']
        hand = match['hand_P2']
        height = match['ht_P2']

    surface = match['surface']
    date = match['date']
    match_id = match['match_id']

    w_df = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) & (db['y'] == 1)) | (db['name_P2'] == name) & (db['y'] == 0)]

    l_df = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) & (db['y'] == 0)) | (db['name_P2'] == name) & (db['y'] == 1)]

    namep1 = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name))]

    namep2 = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P2'] == name))]

    games_played = w_df.shape[0] + l_df.shape[0]
    # random starts
    win_percentage = w_df.shape[0] / games_played if games_played != 0 else 0.1

    surface_win = w_df.loc[w_df['surface'] == surface]
    surface_lose = l_df.loc[l_df['surface'] == surface]

    surface_wins = surface_win.shape[0] / (surface_win.shape[0] + surface_lose.shape[0]) if (
        surface_win.shape[0] + surface_lose.shape[0]) != 0 else 0.1

    if namep1.empty:
        bp_factor = namep2['bpSaved_P2'].mean(
        ) / + namep2['bpFaced_P2'].mean() if namep2['bpFaced_P2'].mean() != 0 else 0.1

        first_won_serve = namep2['1stWon_P2'].mean(
        ) / namep2['1stIn_P2'].mean() if namep2['1stIn_P2'].mean() != 0 else 0.1

        second_won_serve = namep2['2ndWon_P2'].mean(
        ) / + namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1
        ace_probability = namep2['ace_P2'].mean(
        ) / namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1

        double_fault_probability = namep2['df_P2'].mean(
        ) / namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1

        points_on_return = namep2['svpt_P1'].mean(
        ) - namep2['1stWon_P1'].mean() + namep2['2ndWon_P1'].mean()

        serve_points_won = (second_won_serve + first_won_serve) / \
            namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1

        ace_probability = namep2['ace_P1'].mean(
        ) / namep2['svpt_P1'].mean() if namep2['svpt_P1'].mean() != 0 else 0.1


    elif namep2.empty:
        bp_factor = namep1['bpSaved_P1'].mean(
        ) / namep1['bpFaced_P1'].mean() if namep1['bpFaced_P1'].mean() != 0 else 0.1

        first_won_serve = namep1['1stWon_P1'].mean(
        ) / namep1['1stIn_P1'].mean() if namep1['1stIn_P1'].mean() != 0 else 0.1

        second_won_serve = namep1['2ndWon_P1'].mean(
        ) / namep1['svpt_P1'].mean() if namep1['svpt_P1'].mean() != 0 else 0.1

        ace_probability = namep1['ace_P1'].mean(
        ) / namep1['svpt_P1'].mean() if namep1['svpt_P1'].mean() != 0 else 0.1

        double_fault_probability = namep1['df_P1'].mean(
        ) / namep1['svpt_P1'].mean() if namep1['svpt_P1'].mean() != 0 else 0.1

        points_on_return = namep1['svpt_P2'].mean(
        ) - namep1['1stWon_P2'].mean() + namep1['2ndWon_P2'].mean()

        serve_points_won = (second_won_serve + first_won_serve) / \
            namep1['svpt_P1'].mean() if namep1['svpt_P1'].mean() != 0 else 0.1

        ace_probability = namep1['ace_P1'].mean(
        ) / namep1['svpt_P1'].mean() if namep1['svpt_P1'].mean() != 0 else 0.1

    else:
        bp_factor = (namep1['bpSaved_P1'].mean() + namep2['bpSaved_P2'].mean()) / (namep1['bpFaced_P1'].mean() + namep2['bpFaced_P2'].mean()) if (
            namep1['bpFaced_P1'].mean() + namep2['bpFaced_P2'].mean()) != 0 else 0.1

        first_won_serve = (namep1['1stWon_P1'].mean() + namep2['1stWon_P2'].mean()) / (namep1['1stIn_P1'].mean() + namep2['1stIn_P2'].mean()) if (
            namep1['1stIn_P1'].mean() + namep2['1stIn_P2'].mean()) != 0 else 0.1

        second_won_serve = (namep1['2ndWon_P1'].mean() + namep2['2ndWon_P2'].mean()) / (namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) if (
            namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) != 0 else 0.1

        ace_probability = (namep1['ace_P1'].mean() + namep2['ace_P2'].mean()) / (namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) if (
            namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) != 0 else 0.1

        double_fault_probability = (namep1['df_P1'].mean() + namep2['df_P2'].mean()) / (namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) if (
            namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) != 0 else 0.1

        # random done sipko starts
        points_on_return = (namep1['svpt_P2'].mean() - namep1['1stWon_P2'].mean() + namep1['2ndWon_P2'].mean()) + (
            namep2['svpt_P1'].mean() - (namep2['1stWon_P1'].mean() + namep2['2ndWon_P1'].mean()))

        serve_points_won = (second_won_serve + first_won_serve) / (namep1['svpt_P1'].mean(
        ) + namep2['svpt_P2'].mean()) if (namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) != 0 else 0.1

        ace_probability = (namep1['ace_P1'].mean() + namep2['ace_P2'].mean()) / (namep1['svpt_P1'].mean(
        ) + namep2['svpt_P2'].mean()) if (namep1['svpt_P1'].mean() + namep2['svpt_P2'].mean()) != 0 else 0.1

    completeness = points_on_return * serve_points_won
    # sipko done spanias starts
    total_serve_points = first_won_serve + second_won_serve

    aceDf = ace_probability / \
        double_fault_probability if double_fault_probability != 0 else 0.1

    features = pd.DataFrame({
        'match_id': match_id,
        'name': name,
        'rank': rank_official,
        'rank_points': rank_points,
        'elo': rank_elo,
        'glicko': rank_glicko,
        'hand': hand,
        'ht': height,
        'games_played': games_played,
        'win_percentage': win_percentage,
        'surface_wins': surface_wins,
        'bp_factor': bp_factor,
        'first_won_serve': first_won_serve,
        'second_won_serve': second_won_serve,
        'double_fault_probability': double_fault_probability,
        'aceDf': aceDf,
        'points_on_return': points_on_return,
        'serve_points_won': serve_points_won,
        'completeness': completeness,
        'total_serve_points': total_serve_points,
        'ace_probability': ace_probability,
    }, index=[0]
    )

    return features
