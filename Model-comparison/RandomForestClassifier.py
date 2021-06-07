#import packages
import json
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

#read in data
planes_labeled = pd.read_csv("/mnt/data/planes_labeled.csv")

#format data by removing non-numeric columnns and factorize the class
X = planes_labeled.drop(['adshex','class', 'type'], axis = 1)
y = pd.factorize(planes_labeled['class'])[0]

#split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#set a random seed so results will be the same for all of us
np.random.seed(415)

#fit model on training data
my_model = RandomForestClassifier()
my_model.fit(X_train,y_train)

#determine predictions
predictions = my_model.predict(X_test)

#output metrics - here we chose precision and recall
precision = metrics.precision_score(y_true = y_test, y_pred = predictions)
recall = metrics.recall_score(y_true = y_test, y_pred = predictions)

#output metrics to dominostats for display in jobs tab
with open('dominostats.json', 'w') as f:
    f.write(json.dumps({"Precision": precision, "Recall": recall}))