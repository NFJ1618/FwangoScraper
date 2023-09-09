import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import random
# Initial player ratings
ratings = {
    # ... add all players here
}

with open('final_processed.csv', encoding='utf-8') as f:
    data = pd.read_csv(f)
    
X = [i for i in zip(data['Players 1'], data['Players 2'])]
y = [i for i in zip(data['New Score 1'], data['New Score 2'])]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)


def sigmoid(x, coef=0.1):
    return 1/(1+np.exp(-coef*x))

def average_team_rating(p1, p2, ratings):
    if p1 not in ratings:
        ratings[p1] = 100
    if p2 not in ratings:
        ratings[p2] = 100
    return np.mean([ratings[p1], ratings[p2]])

def update_ratings(ratings, team1_p1, team1_p2, team2_p1, team2_p2, predicted, actual, learning_rate):
    error = actual - predicted
    
    # Update ratings with regularization
    ratings[team1_p1] += learning_rate * error
    ratings[team1_p2] += learning_rate * error
    ratings[team2_p1] -= learning_rate * error
    ratings[team2_p2] -= learning_rate * error
    return error







# Dummy training data example:
# Each entry is a tuple (team1, team2, outcome)
# Outcome is 1 if team1 wins, 0 otherwise.

learning_rate = 1
regularization = 0.001
coef = 0.22

def rounds(pred):
    return round(pred)

# Training loop
for _ in range(300):  # Adjust the number of iterations as needed
    train_loss = 0
    train_correct = 0
    train_num = 0
    for match, result in zip(X_train, y_train):
        team1, team2, outcome = match[0], match[1], result[0]
        team1_p1, team1_p2 = team1.split(', ')
        team2_p1, team2_p2 = team2.split(', ')
        avg_rating_team1 = average_team_rating(team1_p1, team1_p2, ratings)
        avg_rating_team2 = average_team_rating(team2_p1, team2_p2, ratings)
        diff = avg_rating_team1 - avg_rating_team2
        pred = sigmoid(diff, coef)
        train_loss += np.abs(update_ratings(ratings, team1_p1, team1_p2, team2_p1, team2_p2, pred, outcome, learning_rate))
        rounded_pred = rounds(pred)
        if rounded_pred == outcome:
            train_correct += 1
        train_num += 1

    test_loss = 0
    test_preds = []
    test_true = []
    for match, result in zip(X_test, y_test):
        team1, team2, outcome = match[0], match[1], result[0]
        team1_p1, team1_p2 = team1.split(', ')
        team2_p1, team2_p2 = team2.split(', ')
        avg_rating_team1 = average_team_rating(team1_p1, team1_p2, ratings)
        avg_rating_team2 = average_team_rating(team2_p1, team2_p2, ratings)
        diff = avg_rating_team1 - avg_rating_team2
        pred = sigmoid(diff)
        test_loss += np.abs(pred-outcome)
        rounded_pred = rounds(pred)
        test_preds.append(rounded_pred)
        test_true.append(outcome)
    
    learning_rate *= 0.99
        
    if _ % 10 == 0:
        print(f'Epoch {_}:')
        print(f'Train loss: {train_loss}')
        print(f"Train accuracy: {train_correct/train_num}")
        print(f'Test loss: {test_loss}')
        # print(f"Test accuracy: {test_correct/test_num}")
        auc = roc_auc_score(test_true, test_preds)
        print(f"Test AUC-ROC: {auc}")

name, rating = [], []
for k, v in ratings.items():
    name.append(k)
    rating.append(v)
a = pd.DataFrame({"Name": name, "Rating": rating})
a.to_csv('ratings.csv')
