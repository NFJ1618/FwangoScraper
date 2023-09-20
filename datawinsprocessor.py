import pandas as pd
import os
import numpy as np



dirs = [
    'casr',
    'ers', 
    'ets',
    'fra',
    'misc',
    'mra',
    'pra',
    'rotc',
    'sts',
    'tasr'
]

dfs = []

for d in dirs:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file == 'games.csv':
                filepath = os.path.join(root, file)
                df = pd.read_csv(filepath)
                dfs.append(df)
                
                
merged_dfs = pd.concat(dfs)

og_tourney_names = set(merged_dfs['Tournament Name'].unique())

should_contain = ['4', '5.0', 'Premier', 'Contender', 'NHZ', 'Gold', 'Challenger', 'Expert']

# Strings that shouldn't be present
should_not_contain = ['Women', 'Mixed']

# Filtering the DataFrame
mask = merged_dfs['Division'].str.contains('|'.join(should_contain))

for string in should_not_contain:
    mask &= ~merged_dfs['Division'].str.contains(string)

filtered_df = merged_dfs[mask]

cur_tourney_names = set(filtered_df['Tournament Name'].unique())

assert len(og_tourney_names-cur_tourney_names) == 0

filtered_df2 = filtered_df[(filtered_df['Score 1'] > 0) | (filtered_df['Score 2'] > 0)]

# print(filtered_df2[filtered_df2['Score 1']==filtered_df2['Score 2']])

assert filtered_df2[filtered_df2['Score 1']==filtered_df2['Score 2']].empty

filtered_df2['New Score 1'] = np.where(filtered_df2['Score 1'] > filtered_df2['Score 2'], 1, 0)
filtered_df2['New Score 2'] = np.where(filtered_df2['Score 2'] > filtered_df2['Score 1'], 1, 0)

final_df = filtered_df2[['Players 1', 'Players 2', 'New Score 1', 'New Score 2']]

def fix_1_more_bug(s):
    if "1 more, " in s:
        return s.replace("1 more, ", "")
    elif "gabe finocchi" in s:
        return s.replace("gabe finocchi", "gabriel finocchi")
    return s


final_df['Players 1'] = final_df['Players 1'].map(fix_1_more_bug)
final_df['Players 2'] = final_df['Players 2'].map(fix_1_more_bug)

final_df.to_csv("final_processed_wins.csv")