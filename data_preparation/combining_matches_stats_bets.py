import pandas as pd  # import pandas library
from date_players_stats import player_stats, player_vs_player, player_bets_stats
from feature_engineering import createFeatures, matchInfo


matches_complete_stats = pd.read_csv(
    'db/created/atp_matches_combined_complete.csv', low_memory=False)

matches_complete_stats['date'] = pd.to_datetime(
    matches_complete_stats['date'], format='%Y%m%d').dt.date  # who knows how in the fuck that solved the problem but it did

# matches_bets_stats = pd.read_csv('db/created/atp_bets_combined.csv')

# matches_bets_stats['Date'] = pd.to_datetime(
#     matches_bets_stats['Date'], format='%Y-%m-%d').dt.date


# atp_matches = atp_matches.set_index(['date'])

# Loop through the matches_complete_stats dataframe and create a new dataframe with average statistics from last 6 months for each player and each match
# That will be preaty sizeble dataframe


matches = matches_complete_stats[['date',
                                  'P1_name', 'P2_name', 'P1_rank_points', 'P2_rank_points', 'surface', 'level']].to_records(index=False)


matches_without_score = pd.DataFrame()


for match in matches[59000:60000]:
    # print(match)

    date = match[0]
    player1 = match[1]
    player2 = match[2]
    p1Points = match[3]
    p2Points = match[4]
    surface = match[5]
    level = match[6]

    player1_stats = createFeatures(
        matches_complete_stats, player1, date, p1Points)

    player2_stats = createFeatures(
        matches_complete_stats, player2, date, p2Points)

    player_stats_merge = pd.merge(
        player1_stats, player2_stats, on='date', suffixes=('_P1', '_P2'))

    player_stats_merge['surface'] = surface
    player_stats_merge['level'] = level
    player_stats_merge['who_won'] = 1

    matches_without_score = pd.concat(
        [player_stats_merge, matches_without_score], ignore_index=True)

    # player_1 = player_stats(matches_complete_stats, player1, date)
    # player_2 = player_stats(matches_complete_stats, player2, date)
    # player_bets_s = player_bets_stats(matches_bets_stats, player1, date)
    # player_vs_player_stats = player_vs_player(
    #     matches_complete_stats, player1, player2, date)

    # print(player_vs_player_stats)

    # print(player_bets_s)
    # print(player_bets_s.size)

    # print('-------------------')


# print(matches_without_score.describe())

matches_without_score.to_csv(
    'db/created/atp_matches_without_score.csv', index=False)
