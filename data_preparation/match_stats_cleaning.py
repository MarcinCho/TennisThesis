"""
Cleans the match stats data and saves it to a new file.

The data is cleaned by removing the following columns:
    - 'tornney_id', 'tournay_name', 'draw_size', 'match_num', 'winner_id', 'winner_seed', 'winner_entry', 'loser_id', 'loser_seed', 'loser_entry', 'best_of', 'round', 'minutes'

"""
import pandas as pd  # import pandas library

# read the csv file
df = pd.read_csv('atp_matches_2022.csv')

# drop the columns
df.drop(['tourney_id', 'tourney_name', 'draw_size', 'match_num', 'winner_id', 'winner_seed', 'winner_entry',
        'loser_id', 'loser_seed', 'loser_entry', 'best_of', 'round', 'minutes'], axis=1, inplace=True)

# save the dataframe to a csv file
df.to_csv('../db/atp/atp_matches_2022_edit.csv', index=False)
