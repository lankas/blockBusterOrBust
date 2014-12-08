"""

 author: Sarah
 script to train an SVM on the movie data and make predictions
 still to-do:
    - cross validation
    - more than just guassian kernel?
    - do freqData and sentimentData

"""

import numpy as np
from sklearn import svm, metrics, grid_search
from sklearn.linear_model import LinearRegression
from freqToData import getData

# saving: http://stackoverflow.com/questions/4450144/easy-save-load-of-data-in-python
#f = open("data", "w")
#f.write("# x y\n")        # column names
#numpy.savetxt(f, numpy.array([x, y]).T)
# loading:
#x, y = numpy.loadtxt("data", unpack=True)

#fileFreq = 'freqMovies.data'
#X = np.loadtxt(fileFreq,delimiter =',')

data = getData('freqTwoWeeks.txt', 'threeClassSkewedRev.txt')
X = data[:,:-1]
y = data[:,-1]
print X.shape, y.shape



#filePerformance = 'performMovies.data'
#y = np.loadtxt(filePerformance,delimiter =',')

n,d = X.shape

#regularlize the data
mean = X.mean(axis=0)
std = X.std(axis=0)
X = (X - mean) / std

#print X

data = getData('freqTwoWeeks.txt', 'revenues.txt')
lin_X = data[:,:-1]
lin_y = data[:,-1]
print lin_X.shape, lin_y.shape

lin_model = svm.SVR(C=1, epsilon=0.2, kernel='linear')
lin_model.fit(lin_X, lin_y)
lin_predictions = lin_model.predict(lin_X)
lin_predictions = lin_predictions.astype(int)
print lin_predictions
lin_accuracy = metrics.accuracy_score(lin_y, lin_predictions)
#lin_precision = metrics.precision_score(lin_y, lin_predictions)
#lin_f1 = metrics.f1_score(lin_y, lin_predictions)

parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'), 'C':[0.001, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

s = svm.SVC()
clf = grid_search.GridSearchCV(s, parameters)
clf.fit(X, y)
print clf.best_estimator_
print "GRID SEARCH: ", clf.best_score_

#predict
C = 0.001 #will do a gridsearch to tune this on testing data
model = svm.SVC(C = C, kernel='rbf', gamma=0.01) #why does this = 2
model.fit(X, y)

predictions = model.predict(X)
test_accuracy = metrics.accuracy_score(y, predictions)
test_precision = metrics.precision_score(y, predictions)
test_f1 = metrics.f1_score(y, predictions)
print "accuracy: ", test_accuracy, lin_accuracy
print "precision: ", test_precision#, lin_precision
print "f1 score: ", test_f1#, lin_f1
