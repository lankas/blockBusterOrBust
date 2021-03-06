"""

 author: Sarah
 script to train an SVM on the movie data and make predictions
 still to-do:
    - cross validation
    - more than just guassian kernel?
    - do freqData and sentimentData

"""
import math
import numpy as np
from sklearn import svm, metrics, grid_search
from sklearn.linear_model import LinearRegression
from freqToData import getData, getWeekData, getTwelveData

# saving: http://stackoverflow.com/questions/4450144/easy-save-load-of-data-in-python
#f = open("data", "w")
#f.write("# x y\n")        # column names
#numpy.savetxt(f, numpy.array([x, y]).T)
# loading:
#x, y = numpy.loadtxt("data", unpack=True)

#fileFreq = 'freqMovies.data'
#X = np.loadtxt(fileFreq,delimiter =',')

X, y = getWeekData('freqTwoWeekInterval.txt', 'threeClassSkewedRev.txt')
# X = data[:,:-1]
# y = data[:,-1]
print X.shape, y.shape



#filePerformance = 'performMovies.data'
#y = np.loadtxt(filePerformance,delimiter =',')

n,d = X.shape

#print X

lin_X, lin_y = getWeekData('freqTwoWeekInterval.txt', 'revenues.txt')
# lin_X = data[:,:-1]
# lin_y = data[:,-1]
print lin_X.shape, lin_y.shape

sentiments = np.loadtxt("sentiments.txt")

# nTrain = int(.6 * 158)
# print "nTrain: ", nTrain

# Xtrain = X[:nTrain,:]
# ytrain = y[:nTrain]
# Xtest = X[nTrain:,:]
# ytest = y[nTrain:]

score = []
squared_mean_error = []
r_squared = []
accuracy = []

idx = np.arange(158)
np.random.shuffle(idx)
X = X[idx]
y = y[idx]
lin_X = lin_X[idx]
lin_y = lin_y[idx]
Xfolds = np.array_split(X, 3)
yfolds = np.array_split(y, 3)
lin_Xfolds = np.array_split(lin_X, 3)
lin_yfolds = np.array_split(lin_y, 3)
sentiments_fold = np.array_split(sentiments, 3)

for j in xrange(3):
	Xtrain = np.concatenate(Xfolds[:j] + Xfolds[j+1:])
	ytrain = np.concatenate(yfolds[:j] + yfolds[j+1:])
	Xtest = Xfolds[j]
	ytest = yfolds[j]

	lin_Xtrain = np.concatenate(lin_Xfolds[:j] + lin_Xfolds[j+1:])
	lin_ytrain = np.concatenate(lin_yfolds[:j] + lin_yfolds[j+1:])
	lin_Xtest = lin_Xfolds[j]
	lin_ytest = lin_yfolds[j]

	sentiments_train = np.concatenate(sentiments_fold[:j] + sentiments_fold[j+1:])
	sentiments_test = sentiments_fold[j]

	#regularlize the data
	mean = Xtrain.mean(axis=0)
	std = Xtrain.std(axis=0)
	Xtrain = (Xtrain - mean) / std
	Xtest = (Xtest - mean) / std


	# lin_Xtrain = lin_X[:nTrain,:]
	# lin_ytrain = lin_y[:nTrain]
	# lin_Xtest = lin_X[nTrain:,:]
	# lin_ytest = lin_y[nTrain:]

	#regularlize the data
	lin_mean = lin_Xtrain.mean(axis=0)
	lin_std = lin_Xtrain.std(axis=0)
	lin_Xtrain = (lin_Xtrain - lin_mean) / lin_std
	lin_Xtest = (lin_Xtest - lin_mean) / lin_std

	lin_model = svm.SVR(C=10, epsilon=0.2, kernel='linear')
	lin_model.fit(lin_Xtrain, lin_ytrain)
	lin_predictions = lin_model.predict(lin_Xtest)
	lin_predictions = lin_predictions.astype(int)
	#print lin_predictions
	score.append(lin_model.score(lin_Xtest, lin_ytest))
	#print "score: ", lin_score
	#lin_accuracy = metrics.accuracy_score(lin_y, lin_predictions)
	squared_mean_error.append(np.sqrt(np.mean(np.square(lin_ytest - lin_predictions))))


	lin_reg = LinearRegression()
	lin_reg.fit(lin_Xtrain, lin_ytrain)
	lin_reg_predictions = lin_model.predict(lin_Xtest).astype(int)
	r_squared.append(np.dot(lin_reg_predictions, lin_ytest) / len(y))
	#print "r squared: ", math.sqrt(lin_reg_r_squared)

	parameters = {'kernel':('linear', 'rbf', 'poly'), 'C':[0.01, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

	# s = svm.SVC()
	# clf = grid_search.GridSearchCV(s, parameters)
	# clf.fit(X, y)
	# print clf.best_estimator_
	# print "GRID SEARCH: ", clf.best_score_

	# clf = grid_search.GridSearchCV(lin_model, parameters)
	# clf.fit(lin_X, lin_y)
	# print clf.best_estimator_
	# print "GRID SEARCH: ", clf.best_score_

	#predict
	C = 0.01 #will do a gridsearch to tune this on testing data
	model = svm.SVC(C = C, kernel='rbf', gamma=2) #why does this = 2
	model.fit(Xtrain, ytrain)

	predictions = model.predict(Xtest)
	test_accuracy = metrics.accuracy_score(ytest, predictions)
	#test_precision = metrics.precision_score(y, predictions)
	#test_f1 = metrics.f1_score(y, predictions)
	accuracy.append(test_accuracy)
	#print "accuracy: ", test_accuracy
	#print "precision: ", test_precision#, lin_precision
	#print "f1 score: ", test_f1#, lin_f1

print "score: ", np.mean(score)
print "squared mean error: ", np.mean(squared_mean_error)
print "r_squared: ", np.mean(r_squared)
print "accuracy: ", np.mean(accuracy)


