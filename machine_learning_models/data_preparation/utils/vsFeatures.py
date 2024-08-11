import pandas as pd

time_f = pd.Timedelta(days=365)


def vsfeatureCreator(db):

    vs_features = pd.DataFrame()
    pvp = 0
    common = 0
    missing = 0

    for id, match in db.iterrows():
        date = match['date']
        name = match['name_P1']
        name2 = match['name_P2']

        op_list = common_opponent(match, db)

        search_pvp = db.loc[(db['date'] > (
            date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) & (db['name_P2'] == name2)) | ((db['name_P1'] == name2) & (db['name_P2'] == name))]

        if not search_pvp.empty:
            p1_features = pvp_stats(search_pvp, name, match['match_id'])
            p2_features = pvp_stats(search_pvp, name2, match['match_id'])
            vs_f = pd.merge(p1_features, p2_features,
                            on='match_id', suffixes=('_P1', '_P2'))
            vs_features = pd.concat([vs_features, vs_f], ignore_index=True)
            pvp += 1
        elif len(op_list) != 0:
            p1_features = pd.DataFrame()
            p2_features = pd.DataFrame()
            common += 1

            for opponent in op_list[:1]:
                search_common_P1 = db.loc[(db['date'] > (
                    date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) & (db['name_P2'] == opponent)) | ((db['name_P1'] == opponent) & (db['name_P2'] == name))]

                search_common_P2 = db.loc[(db['date'] > (date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name2) & (
                    db['name_P2'] == opponent)) | ((db['name_P1'] == opponent) & (db['name_P2'] == name2))]

                p1_features = pd.concat([pvp_stats(
                    search_common_P1, opponent, match['match_id']), p1_features], ignore_index=True)
                p2_features = pd.concat([pvp_stats(
                    search_common_P2, opponent, match['match_id']), p2_features],    ignore_index=True)

                if search_common_P1.empty or search_common_P2.empty:
                    print('cos przerywa w common opponent')

            p1_features = p1_features.mean().to_frame().T
            p1_features['match_id'] = match['match_id']
            p2_features = p2_features.mean().to_frame().T
            p2_features['match_id'] = match['match_id']
            vs_f = pd.merge(p1_features, p2_features,
                            on='match_id', suffixes=('_P1', '_P2'))
            vs_features = pd.concat([vs_features, vs_f], ignore_index=True)
        else:
            missing += 1

        # else:
        #     avg_P1 = db.loc[(db['date'] > (
        #         date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) & (db['ELO_P2'] >= match['ELO_P2'] - 50) & (db['ELO_P2'] <= match['ELO_P2'] - 50) | (db['name_P2'] == name) & (db['ELO_P1'] >= match['ELO_P1'] - 50) & (db['ELO_P1'] <= match['ELO_P1'] - 50))]
        #     avg_P2 = db.loc[(db['date'] > (date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name2) & (db['ELO_P2'] >= match['ELO_P2'] - 50) & (
        #         db['ELO_P2'] <= match['ELO_P2'] - 50) | (db['name_P2'] == name2) & (db['ELO_P1'] >= match['ELO_P1'] - 50) & (db['ELO_P1'] <= match['ELO_P1'] - 50))]

        #     if avg_P1.empty or avg_P2.empty:
        #         avg_P1 = db.loc[(db['date'] < date) & (
        #             (db['name_P1'] == name) | (db['name_P2'] == name))]
        #         avg_P2 = db.loc[(db['date'] < date) & (
        #             (db['name_P1'] == name2) | (db['name_P2'] == name2))]
        #         if avg_P1.empty or avg_P2.empty:
        #             print('cos przerywa w walku ELO')
        #         else:
        #             p1_features = pvp_stats(avg_P1, name, match['match_id'])
        #             p2_features = pvp_stats(avg_P2, name2, match['match_id'])
        #             vs_f = pd.merge(p1_features, p2_features,
        #                             on='match_id', suffixes=('_P1', '_P2'))
        #             vs_features = pd.concat(
        #                 [vs_features, vs_f], ignore_index=True)
        #     else:
        #         p1_features = pvp_stats(avg_P1, name, match['match_id'])
        #         p2_features = pvp_stats(avg_P2, name2, match['match_id'])
        #         vs_f = pd.merge(p1_features, p2_features,
        #                         on='match_id', suffixes=('_P1', '_P2'))
        #         vs_features = pd.concat([vs_features, vs_f], ignore_index=True)

    print('pvp: ', pvp)
    print('common: ', common)
    print('missing: ', missing)

    return vs_features


def pvp_stats(db, name, match_id):
    w_df = db.loc[((db['name_P1'] == name) & (db['y'] == 1))
                  | (db['name_P2'] == name) & (db['y'] == 0)]

    l_df = db.loc[((db['name_P1'] == name) & (db['y'] == 0))
                  | (db['name_P2'] == name) & (db['y'] == 1)]

    games_played = w_df.shape[0] + l_df.shape[0]

    win_percentage = w_df.shape[0] / games_played if games_played != 0 else 0.1

    namep1 = db.loc[(db['name_P1'] == name)]

    namep2 = db.loc[(db['name_P2'] == name)]

    if namep1.empty:

        bp_factor = namep2['bpSaved_P2'].mean(
        ) / namep2['bpFaced_P2'].mean() if (namep2['bpFaced_P2'].mean()) != 0 else 0.1
        first_won_serve = namep2['1stWon_P2'].mean(
        ) / namep2['1stIn_P2'].mean() if namep2['1stIn_P2'].mean() != 0 else 0.1

        second_won_serve = namep2['2ndWon_P2'].mean(
        ) / namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1

        ace_probability = namep2['ace_P2'].mean(
        ) / namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1

        double_fault_probability = namep2['df_P2'].mean(
        ) / namep2['svpt_P2'].mean() if namep2['svpt_P2'].mean() != 0 else 0.1
        aceDf = ace_probability / \
            double_fault_probability if double_fault_probability != 0 else 0.1

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

        aceDf = ace_probability / \
            double_fault_probability if double_fault_probability != 0 else 0.1

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

        aceDf = ace_probability / \
            double_fault_probability if double_fault_probability != 0 else 0.1

    features = pd.DataFrame({
        'match_id': match_id,
        'win_percentage': win_percentage,
        'bp_factor': bp_factor,
        'first_won_serve': first_won_serve,
        'second_won_serve': second_won_serve,
        'ace_probability': ace_probability,
        'double_fault_probability': double_fault_probability,
        'aceDf': aceDf,
    }, index=[0]
    )

    return features


def common_opponent(match, db):
    date = match['date']
    name = match['name_P1']
    name2 = match['name_P2']

    player1_df = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name) | (db['name_P2'] == name)) & ((db['name_P1'] != name2) & (db['name_P2'] != name2))]

    player2_df = db.loc[(db['date'] > (
        date - time_f)) & (db['date'] < date) & ((db['name_P1'] == name2) | (db['name_P2'] == name2)) & ((db['name_P1'] != name) & (db['name_P2'] != name))]

    player1_opponents = player1_df['name_P1'].unique().tolist() + \
        player1_df['name_P2'].unique().tolist()
    player2_opponents = player2_df['name_P1'].unique().tolist() + \
        player2_df['name_P2'].unique().tolist()

    search_common = list(set(player1_opponents) &
                         set(player2_opponents))

    search_common = set(search_common)

    search_common = list(search_common)

    return search_common
