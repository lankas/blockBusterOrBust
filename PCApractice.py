from sklearn.decomposition import PCA
from freqToData import getData
from sklearn.linear_model import LinearRegression
from sklearn import svm, metrics, grid_search
import numpy as np
import math

X, y = getData('freqOneWeek.txt', 'threeClassSkewedRev.txt')
# X = data[:,:-1]
# y = data[:,-1]

lin_X, lin_y = getData('freqOneWeek.txt', 'revenues.txt')
# lin_X = data[:,:-1]
# lin_y = data[:,-1]

nTrain = int(.6 * 158)

sentiments = np.loadtxt("sentiments.txt")

np.random.seed(3)

pca_explained = []
pca_lin_explained = []
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

	mean = Xtrain.mean(axis=0)
	std = Xtrain.std(axis=0)
	Xtrain = (Xtrain - mean) / std
	Xtest = (Xtest - mean) / std

	lin_mean = lin_Xtrain.mean(axis=0)
	lin_std = lin_Xtrain.std(axis=0)
	lin_Xtrain = (lin_Xtrain - lin_mean) / lin_std
	lin_Xtest = (lin_Xtest - lin_mean) / lin_std

	pca = PCA(n_components = 12)
	pcaTransformer = pca.fit(Xtrain)
	Xt_train = pcaTransformer.transform(Xtrain)
	pca_explained.append(sum(pca.explained_variance_ratio_))
	#print "PCA:", sum(pca.explained_variance_ratio_)
	Xt_test = pcaTransformer.transform(Xtest)

	pca_lin = PCA(n_components = 12)
	pcaTransformer_lin = pca_lin.fit(lin_Xtrain)
	Xt_lin_train = pcaTransformer_lin.transform(lin_Xtrain)
	Xt_lin_test = pcaTransformer_lin.transform(lin_Xtest)
	pca_lin_explained.append(sum(pca_lin.explained_variance_ratio_))
	#print "PCA lin:", sum(pca_lin.explained_variance_ratio_)

	print Xt_train.shape, sentiments_train.shape

	Xt_train = np.hstack((Xt_train, sentiments_train))
	Xt_test = np.hstack((Xt_test, sentiments_test))
	Xt_lin_train = np.hstack((Xt_lin_train, sentiments_train))
	Xt_lin_test = np.hstack((Xt_lin_test, sentiments_test))

	print Xt_lin_train, Xt_lin_train.shape
	print lin_ytrain.shape


	lin_model = svm.SVR(C=10, epsilon=0.1, kernel='rbf')
	lin_model.fit(Xt_lin_train, lin_ytrain)
	lin_predictions = lin_model.predict(Xt_lin_test)
	lin_predictions = lin_predictions.astype(int)
	#print lin_predictions
	lin_accuracy = metrics.accuracy_score(lin_ytest, lin_predictions)

	score.append(lin_model.score(Xt_lin_test,lin_ytest))
	#print "score: ", lin_model.score(Xt_lin_test,lin_ytest)

	#print "squared mean error: ", np.sqrt(np.mean(np.square(lin_ytest - lin_predictions))), np.mean(lin_ytest)
	squared_mean_error.append(np.sqrt(np.mean(np.square(lin_ytest - lin_predictions))))

	parameters = {'kernel':('poly','linear'), 'C':[0.001, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

	lin_reg = LinearRegression()
	lin_reg.fit(Xt_lin_train, lin_ytrain)
	lin_reg_predictions = lin_model.predict(Xt_lin_test).astype(int)
	lin_reg_r_squared = np.dot(lin_reg_predictions, lin_ytest) / len(y)
	#print "r squared: ", math.sqrt(lin_reg_r_squared)
	r_squared.append(math.sqrt(lin_reg_r_squared))


	#s = svm.SVC()
	#clf = grid_search.GridSearchCV(s, parameters)
	#clf.fit(X, y)
	#print clf.best_estimator_
	#print "GRID SEARCH: ", clf.best_score_

	C = 1 #will do a gridsearch to tune this on testing data
	model = svm.SVC(C = C, kernel='rbf', degree=2, gamma=0.1) 
	model.fit(Xt_train, ytrain)

	predictions = model.predict(Xt_test)
	test_accuracy = metrics.accuracy_score(ytest, predictions)
	#test_precision = metrics.precision_score(ytest, predictions)
	#test_f1 = metrics.f1_score(ytest, predictions)

	accuracy.append(test_accuracy)
	#print "accuracy: ", test_accuracy

print "pca_lin: ", np.mean(pca_lin_explained)
print "pca: ", np.mean(pca_lin_explained)
print "score: ", np.mean(score)
print "squared mean error: ", np.mean(squared_mean_error)
print "r_squared: ", np.mean(r_squared)
print "accuracy: ", np.mean(accuracy)
