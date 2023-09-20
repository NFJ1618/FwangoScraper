import numpy as np

def bucket_divisions(filtered_df):
    top_should_have = ['Premier', 'Pro']
    high_should_have = ['Gold', '5.', 'Expert']
    high_should_not_have = ['4.', '3.']
    medium_should_have = ['Contender', '4.', 'Challenger']
    medium_should_not_have = ['3.']
    low = ['3', 'Advanced']

    conditions = [
        filtered_df['Division'].str.contains('|'.join(top_should_have)),
        filtered_df['Division'].str.contains('|'.join(high_should_have)) & ~filtered_df['Division'].str.contains('|'.join(high_should_not_have)),
        filtered_df['Division'].str.contains('|'.join(medium_should_have)) & ~filtered_df['Division'].str.contains('|'.join(medium_should_not_have)),
        filtered_df['Division'].str.contains('|'.join(low)),
    ]

    # Corresponding values for each condition
    choices = ['Top','High',  'Medium', 'Low']

    filtered_df['Category'] = np.select(conditions, choices, default='Other')
    return filtered_df


def predict(team1_p1, team1_p2, team2_p1, team2_p2, pow_factor=100, w=0.7):
    ep1 = ((1/(1+pow(10, (team2_p1-team1_p1)/pow_factor)))+(1/(1+pow(10, (team2_p2-team1_p1)/pow_factor))))/2
    ep2 = ((1/(1+pow(10, (team2_p1-team1_p2)/pow_factor)))+(1/(1+pow(10, (team2_p2-team1_p2)/pow_factor))))/2
    ep3 = ((1/(1+pow(10, (team1_p1-team2_p1)/pow_factor)))+(1/(1+pow(10, (team1_p2-team2_p1)/pow_factor))))/2
    ep4 = ((1/(1+pow(10, (team1_p1-team2_p2)/pow_factor)))+(1/(1+pow(10, (team1_p2-team2_p2)/pow_factor))))/2

    team1_stronger_ep = max(ep1, ep2)
    team1_weaker_ep = min(ep1, ep2)
    team2_stronger_ep = max(ep3, ep4)
    team2_weaker_ep = min(ep3, ep4)
    
    et1 = w * team1_stronger_ep + (1 - w) * team1_weaker_ep
    et2 = w * team2_stronger_ep + (1 - w) * team2_weaker_ep

    return et1, et2, ep1, ep2, ep3, ep4
