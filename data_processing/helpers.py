import numpy as np

def bucket_divisions(filtered_df):
    top_should_have = ['Premier', 'Pro', '5.0+']
    top_should_not_have = ['4.']
    high_should_have = ['Gold', '5.', '4.5', 'Expert', 'Contender', 'Challenger']
    high_should_not_have = ['4.0', '3.']
    medium_should_have = ['4.0', 'Advanced']
    medium_should_not_have = ['3.']
    low = ['3']

    conditions = [
        filtered_df['Division'].str.contains('|'.join(top_should_have)) & ~filtered_df['Division'].str.contains('|'.join(top_should_not_have)),
        filtered_df['Division'].str.contains('|'.join(high_should_have)) & ~filtered_df['Division'].str.contains('|'.join(high_should_not_have)),
        filtered_df['Division'].str.contains('|'.join(medium_should_have)) & ~filtered_df['Division'].str.contains('|'.join(medium_should_not_have)),
        filtered_df['Division'].str.contains('|'.join(low)),
    ]

    # Corresponding values for each condition
    choices = ['Top','High',  'Medium', 'Low']

    filtered_df['Category'] = np.select(conditions, choices, default='Other')
    return filtered_df




def fix_1_more_bug(s):
    maps = {
        "1 more, ": "",
        "gabe finocchi": "gabriel finocchi",
        "coleman epperson's": "coleman epperson"
    }
    for i in maps.keys():
        if i in s:
            s = s.replace(i, maps[i])
    return s