from sklearn.decomposition import PCA
from freqToData import getData
from sklearn.linear_model import LinearRegression
from sklearn import svm, metrics, grid_search
import numpy as np
import math

data = getData('freqOneWeek.txt', 'threeClassSkewedRev.txt')
X = data[:,:-1]
y = data[:,-1]

data = getData('freqOneWeek.txt', 'revenues.txt')
lin_X = data[:,:-1]
lin_y = data[:,-1]

nTrain = int(.6 * 158)

Xtrain = X[:nTrain,:]
ytrain = y[:nTrain]
Xtest = X[nTrain:,:]
ytest = y[nTrain:]

lin_Xtrain = lin_X[:nTrain,:]
lin_ytrain = lin_y[:nTrain]
lin_Xtest = lin_X[nTrain:,:]
lin_ytest = lin_y[nTrain:]

pca = PCA(n_components = 12)
pcaTransformer = pca.fit(Xtrain)
Xt_train = pcaTransformer.transform(Xtrain)
print "PCA:", sum(pca.explained_variance_ratio_)
Xt_test = pcaTransformer.transform(Xtest)

pca_lin = PCA(n_components = 12)
pcaTransformer_lin = pca_lin.fit(lin_Xtrain)
Xt_lin_train = pcaTransformer_lin.transform(lin_Xtrain)
Xt_lin_test = pcaTransformer_lin.transform(lin_Xtest)
print "PCA lin:", sum(pca_lin.explained_variance_ratio_)

lin_model = svm.SVR(C=1, epsilon=0.2, kernel='linear')
lin_model.fit(Xt_lin_train, lin_ytrain)
lin_predictions = lin_model.predict(Xt_lin_test)
lin_predictions = lin_predictions.astype(int)
#print lin_predictions
lin_accuracy = metrics.accuracy_score(lin_ytest, lin_predictions)

print "score: ", lin_model.score(Xt_lin_test,lin_ytest)

print np.sqrt(np.mean(np.square(lin_ytest - lin_predictions))), np.mean(lin_ytest)


parameters = {'kernel':('poly','linear'), 'C':[0.001, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

lin_reg = LinearRegression()
lin_reg.fit(Xt_lin_train, lin_ytrain)
lin_reg_predictions = lin_model.predict(Xt_lin_test).astype(int)
lin_reg_r_squared = np.dot(lin_reg_predictions, lin_ytest) / len(y)
print "r squared: ", math.sqrt(lin_reg_r_squared)



#s = svm.SVC()
#clf = grid_search.GridSearchCV(s, parameters)
#clf.fit(X, y)
#print clf.best_estimator_
#print "GRID SEARCH: ", clf.best_score_

C = 0.01 #will do a gridsearch to tune this on testing data
model = svm.SVC(C = C, kernel='poly', degree=3) 
model.fit(Xt_train, ytrain)

predictions = model.predict(Xt_test)
test_accuracy = metrics.accuracy_score(ytest, predictions)
test_precision = metrics.precision_score(ytest, predictions)
test_f1 = metrics.f1_score(ytest, predictions)

print "accuracy: ", test_accuracy


#st = svm.SVC()
#clft = grid_search.GridSearchCV(st, parameters)
#clft.fit(Xt, y)
#print clft.best_estimator_
#print "PCA GRID SEAsRCH: ", clft.best_score_
