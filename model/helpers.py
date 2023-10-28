import numpy as np

def predict_points(team1_p1, team1_p2, team2_p1, team2_p2, pow_factor=100, w=0.7):
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


def predict_wins(team1_p1, team1_p2, team2_p1, team2_p2, sigmoid_coef=0.1, w=0.7):
    team1_stronger_ep = max(team1_p1, team1_p2)
    team1_weaker_ep = min(team1_p1, team1_p2)
    team2_stronger_ep = max(team2_p1, team2_p2)
    team2_weaker_ep = min(team2_p1, team2_p2)
    
    et1 = w * team1_stronger_ep + (1 - w) * team1_weaker_ep
    et2 = w * team2_stronger_ep + (1 - w) * team2_weaker_ep

    pred = sigmoid(et1-et2, sigmoid_coef)

    return pred, et1, et2

def game_regularization(n, k, a):
    return int(np.exp(-k*(n-a)))



def sigmoid(x, coef=0.1):
    return 1/(1+np.exp(-coef*x))