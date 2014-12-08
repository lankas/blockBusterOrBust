from sklearn.decomposition import PCA
from freqToData import getData
from sklearn import svm, metrics, grid_search

data = getData('freqTwoWeeks.txt', 'threeClassSkewedRev.txt')
X = data[:,:-1]
y = data[:,-1]

pca = PCA(n_components = 10)

pcaTransformer = pca.fit(X)

Xt = pcaTransformer.transform(X)

print "PCA:", sum(pca.explained_variance_ratio_)


parameters = {'kernel':('linear', 'rbf', 'poly', 'sigmoid'), 'C':[0.001, 10], 'gamma':[0.01, 10], 'degree':[3, 5]}

#s = svm.SVC()
#clf = grid_search.GridSearchCV(s, parameters)
#clf.fit(X, y)
#print clf.best_estimator_
#print "GRID SEARCH: ", clf.best_score_


st = svm.SVC()
clft = grid_search.GridSearchCV(st, parameters)
clft.fit(Xt, y)
print clft.best_estimator_
print "PCA GRID SEARCH: ", clft.best_score_
