import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

dataset = pd.read_csv('/content/2020_bn_nb_data.txt', delimiter='\t')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

label_encoder_1 = LabelEncoder()
label_encoder_2 = LabelEncoder()

for i in range(X.shape[1]):
    X[:, i] = label_encoder_1.fit_transform(X[:, i])

y = label_encoder_2.fit_transform(y)

accuracy_scores = []

for i in range(20):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=i)
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracy_scores.append(accuracy)

print("Accuracy scores for each iteration:")
for i, score in enumerate(accuracy_scores):
    print(f"Iteration {i + 1}: {score}")

print(f"\nAverage accuracy: {np.mean(accuracy_scores)}")
