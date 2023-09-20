import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from random import shuffle
import random
from unidecode import unidecode
# Initial player ratings
import sys

class Ratings:
    def __init__(self) -> None:
        self.ratings = {}
        
    def __getitem__(self, index):
	    # Your Implementation
        if index not in self.ratings:
            self.ratings[index] = 100
        return self.ratings[index]
    
    def __setitem__(self, key, value):
	    # Your Implementation
        self.ratings[key] = value
    
    def items(self):
        return self.ratings.items()

class Model:
    def __init__(self, file, points: bool, learning_rate = 5, rating_regularization = 0.001, decay=1, test_size=0.1, k=0.1, a=46, test=True, game_reg=True, pow_factor=100):
        self.test = test
        self.ratings = Ratings()
        self.lr = learning_rate
        self.decay = decay
        self.pow_factor = pow_factor
        self.k=0.1
        self.a=46
        self.game_reg = game_reg
        if not self.game_reg:
            self.k = 0
        if points:
            self.lr = 1
        else:
            self.lr = 0.1
            
        self.weights = {
            'Win': {
                'Top': 1, 
                'High': 0.8,
                'Medium': 0.6,
                'Low': 0.4
            },
            'Loss': {
                'Top': 0.6, 
                'High': 0.7,
                'Medium': 0.8,
                'Low': 1
            }
        }        
    
        self.points = points
        self.rate_reg = rating_regularization
        self.games = {
            
        }

        with open(file, encoding='utf-8') as f:
            self.data = pd.read_csv(f)
    
        self.X = [i for i in zip(self.data['Players 1'], self.data['Players 2'])]
        self.y = [i for i in zip(self.data['New Score 1'], self.data['New Score 2'], self.data['Category'])]

        if self.test:
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=test_size)
        else:
            self.X_train = self.X
            self.y_train = self.y


        for team1, team2 in self.X_train:
            team1_p1, team1_p2 = team1.split(', ')
            team2_p1, team2_p2 = team2.split(', ')
            a = [team1_p1, team1_p2, team2_p1, team2_p2]
            for i in a:
                if i in self.games:
                    self.games[i] += 1
                else:
                    self.games[i] = 1

    def sigmoid(self, x, coef=0.1):
        return 1/(1+np.exp(-coef*x))

    def predict(self, team1_p1, team1_p2, team2_p1, team2_p2):
        pow_factor=self.pow_factor
        ep1 = ((1/(1+pow(10, (team2_p1-team1_p1)/pow_factor)))+(1/(1+pow(10, (team2_p2-team1_p1)/pow_factor))))/2
        ep2 = ((1/(1+pow(10, (team2_p1-team1_p2)/pow_factor)))+(1/(1+pow(10, (team2_p2-team1_p2)/pow_factor))))/2
        ep3 = ((1/(1+pow(10, (team1_p1-team2_p1)/pow_factor)))+(1/(1+pow(10, (team1_p2-team2_p1)/pow_factor))))/2
        ep4 = ((1/(1+pow(10, (team1_p1-team2_p2)/pow_factor)))+(1/(1+pow(10, (team1_p2-team2_p2)/pow_factor))))/2
        et1 = (ep1+ep2)/2
        et2 = (ep3+ep4)/2
        return et1, et2, ep1, ep2, ep3, ep4

    def average_team_rating(self, p1, p2, ratings, factor):
        if p1 not in ratings:
            ratings[p1] = 100
        if p2 not in ratings:
            ratings[p2] = 100
        a = [ratings[p1], ratings[p2]]
        higher = max(a)
        lower = min(a)
        return factor * higher + (1-factor) * lower

    def update_ratings(self, team1_p1, team1_p2, team2_p1, team2_p2, predicted, actual, category):
        error = actual - predicted
        # Modify learning rate based on outcome and prediction
        magnitude = abs(predicted - 0.5)  # How close the prediction is to being uncertain
        if (predicted > 0.5 and actual < predicted) or (predicted < 0.5 and actual > predicted):  
            # If outcome is surprising (i.e., underdog wins or strong team loses)
            magnitude_multiplier = 1 + magnitude  # Increase the magnitude if the difference is larger
        else:
            magnitude_multiplier = 1 - magnitude  # Decrease the magnitude if the difference is smaller
        
        dynamic_lr = self.lr * magnitude_multiplier
        
        if actual > 0.5:
            team1_weight = self.weights['Win'][category]
            team2_weight = self.weights['Loss'][category]
        else:
            team2_weight = self.weights['Win'][category]
            team1_weight = self.weights['Loss'][category]

        self.ratings[team1_p1] = self.ratings[team1_p1] + dynamic_lr * error * team1_weight
        self.ratings[team1_p2] = self.ratings[team1_p2] + dynamic_lr * error * team1_weight
        self.ratings[team2_p1] = self.ratings[team2_p1] - dynamic_lr * error * team2_weight
        self.ratings[team2_p2] = self.ratings[team2_p2] - dynamic_lr * error * team2_weight
        return error


    def game_regularization(self, n):
        return int(np.exp(-self.k*(n-self.a)))

    def rounds(self, pred):
        return round(pred)

    # Training loop
    def train(self, n_iters: int):
        for _ in range(n_iters):  # Adjust the number of iterations as needed
            train_loss = 0
            train_correct = 0
            train_num = 0
            for match, result in zip(self.X_train, self.y_train):
                team1, team2, team1_score, team2_score, category = match[0], match[1], int(result[0]), int(result[1]), result[2]
                team1_p1, team1_p2 = team1.split(', ')
                team2_p1, team2_p2 = team2.split(', ')

                
                if self.points:
                    preds = self.predict(self.ratings[team1_p1], self.ratings[team1_p2], self.ratings[team2_p1], self.ratings[team2_p2])
                    pred = preds[0]
                    outcome = team1_score/(team1_score+team2_score)
                else:
                    preds = self.predict(self.ratings[team1_p1], self.ratings[team1_p2], self.ratings[team2_p1], self.ratings[team2_p2])
                    pred = preds[0]
                    outcome = team1_score
                train_loss += np.abs(self.update_ratings(team1_p1, team1_p2, team2_p1, team2_p2, pred, outcome, category))
                rounded_pred = self.rounds(pred)
                processed_outcome = 1 if team1_score > team2_score else 0
                if rounded_pred == processed_outcome:
                    train_correct += 1
                train_num += 1
            train_loss /= len(self.X_train)

            if self.test:
                test_loss = 0
                test_preds = []
                test_true = []
                test_acc = []
                for match, result in zip(self.X_test, self.y_test):
                    team1, team2, team1_score, team2_score = match[0], match[1], int(result[0]), int(result[1])
                    team1_p1, team1_p2 = team1.split(', ')
                    team2_p1, team2_p2 = team2.split(', ')
                    if self.points:
                        preds = self.predict(self.ratings[team1_p1], self.ratings[team1_p2], self.ratings[team2_p1], self.ratings[team2_p2])
                        pred = preds[0]
                        outcome = team1_score/(team1_score+team2_score)
                    else:
                        preds = self.predict(self.ratings[team1_p1], self.ratings[team1_p2], self.ratings[team2_p1], self.ratings[team2_p2])
                        pred = preds[0]
                        outcome = team1_score
                    test_loss += np.abs(pred-outcome)
                    rounded_pred = self.rounds(pred)
                    processed_outcome = 1 if team1_score > team2_score else 0
                    test_preds.append(rounded_pred)
                    test_true.append(processed_outcome)
                    test_acc.append(rounded_pred==processed_outcome)
                test_loss /= len(self.X_test)
            self.lr *= self.decay
                
            if _ % 10 == 0:
                print(f'Epoch {_}:')
                print(f'Train loss: {train_loss}')
                print(f"Train accuracy: {train_correct/train_num}")
                if self.test:
                    print(f'Test loss: {test_loss}')
                    print(f"Test accuracy: {sum(test_acc)/len(test_acc)}")
                    auc = roc_auc_score(test_true, test_preds)
                    print(f"Test AUC-ROC: {auc}")


    def output(self, file_name):
        name, rating, adjusted_rating, num_games = [], [], [], []
        for k, v in self.ratings.items():
            name.append(unidecode(k))
            adjusted_rating.append((v*self.games[k]+100*self.game_regularization(self.games[k]))/(self.game_regularization(self.games[k])+self.games[k]))
            rating.append(v)
            num_games.append(self.games[k])
        a = pd.DataFrame({"Name": name, "Rating": rating, "Adjusted Rating": adjusted_rating, "Games": num_games})
        a = a.sort_values(by='Adjusted Rating', ascending=False)
        a.to_csv(file_name)


if __name__ == '__main__':
    points = True
    if points:
        infile = 'final_processed_points.csv'
        outfile = 'points_ratings.csv'
    else:
        infile = 'final_processed_wins.csv'
        outfile = 'wins_ratings.csv'
    
    
    model = Model(infile, points=points, k=0.04, a=100, test=True, game_reg=True)
    model.train(200)
    model.output(outfile)