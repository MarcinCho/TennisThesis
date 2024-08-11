import zipfile
import pandas as pd  # import pandas library
import os

import urllib3


# https://github.com/JeffSackmann/tennis_atp

# https://github.com/JeffSackmann/tennis_atp/archive/refs/heads/master.zip

path = "db/atp"
files = os.listdir(path)


url = "https://github.com/JeffSackmann/tennis_atp/archive/refs/heads/master.zip"
repo = urllib3.request("GET", url)
repo_zip = repo.read()

matches = zipfile.ZipFile(repo_zip)

import zipfile
import pandas as pd  # import pandas library
import os
import urllib3

# https://github.com/JeffSackmann/tennis_atp

# https://github.com/JeffSackmann/tennis_atp/archive/refs/heads/master.zip

path = "db/atp"
files = os.listdir(path)

url = "https://github.com/JeffSackmann/tennis_atp/archive/refs/heads/master.zip"
repo = urllib3.request("GET", url)
with open("repo.zip", "wb") as f:
    f.write(repo.read())

matches = zipfile.ZipFile("repo.zip")

print(files)

combined_years_df = pd.concat(
    [pd.read_csv(f"{path}/{file}") for file in files if file.endswith(".csv")],
    ignore_index=True,
)

print(files)

combined_years_df = pd.concat(
    [pd.read_csv(f"{path}/{file}") for file in files if file.endswith(".csv")],
    ignore_index=True,
)

print(combined_years_df.head())
print(combined_years_df.shape)

combined_years_df.rename(
    columns={
        "tourney_date": "date",
        "tourney_level": "level",
        "draw_size": "draw_size",
        "winner_name": "P1_name",
        "winner_seed": "P1_seed",
        "winner_hand": "P1_hand",
        "winner_ht": "P1_ht",
        "winner_age": "P1_age",
        "winner_rank": "P1_rank",
        "winner_rank_points": "P1_rank_points",
        "loser_name": "P2_name",
        "loser_seed": "P2_seed",
        "loser_hand": "P2_hand",
        "loser_ht": "P2_ht",
        "loser_rank": "P2_rank",
        "loser_rank_points": "P2_rank_points",
    },
    inplace=True,
)


combined_years_df.to_csv("db/created/atp_matches_combined_complete.csv", index=False)
