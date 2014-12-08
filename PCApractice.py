from sklearn.decomposition import PCA
from freqToData import getData
from sklearn import svm, metrics, grid_search
import numpy as np

data = getData('freqTwoWeeks.txt', 'threeClassSkewedRev.txt')
X = data[:,:-1]
y = data[:,-1]

data = getData('freqTwoWeeks.txt', 'revenues.txt')
lin_X = data[:,:-1]
lin_y = data[:,-1]

pca = PCA(n_components = 25)
pcaTransformer = pca.fit(X)
Xt = pcaTransformer.transform(X)
print "PCA:", sum(pca.explained_variance_ratio_)

pca_lin = PCA(n_components = 25)
pcaTransformer_lin = pca_lin.fit(lin_X)
Xt_lin = pcaTransformer.transform(lin_X)
print "PCA lin:", sum(pca_lin.explained_variance_ratio_)

lin_model = svm.SVR(C=1, epsilon=0.2, kernel='linear')
lin_model.fit(Xt_lin, lin_y)
lin_predictions = lin_model.predict(Xt_lin)
lin_predictions = lin_predictions.astype(int)
print lin_predictions
lin_accuracy = metrics.accuracy_score(lin_y, lin_predictions)

print lin_model.score(Xt_lin,lin_y)

print np.sqrt(np.mean(np.square(lin_y - lin_predictions))), np.mean(lin_y)


parameters = {'kernel':('poly','linear'), 'C':[0.001, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

#s = svm.SVC()
#clf = grid_search.GridSearchCV(s, parameters)
#clf.fit(X, y)
#print clf.best_estimator_
#print "GRID SEARCH: ", clf.best_score_

C = 0.01 #will do a gridsearch to tune this on testing data
model = svm.SVC(C = C, kernel='poly', degree=3) 
model.fit(Xt[1:100], y[1:100])

predictions = model.predict(Xt[100:])
test_accuracy = metrics.accuracy_score(y[100:], predictions)
test_precision = metrics.precision_score(y[100:], predictions)
test_f1 = metrics.f1_score(y[100:], predictions)

print test_accuracy


st = svm.SVC()
#clft = grid_search.GridSearchCV(st, parameters)
#clft.fit(Xt, y)
#print clft.best_estimator_
#print "PCA GRID SEAsRCH: ", clft.best_score_
