"""

 author: Sarah
 script to train an SVM on the movie data and make predictions
 still to-do:
    - cross validation
    - more than just guassian kernel?
    - do freqData and sentimentData

"""

import numpy as np
from sklearn import svm, metrics

# saving: http://stackoverflow.com/questions/4450144/easy-save-load-of-data-in-python
#f = open("data", "w")
#f.write("# x y\n")        # column names
#numpy.savetxt(f, numpy.array([x, y]).T)
# loading:
#x, y = numpy.loadtxt("data", unpack=True)

fileFreq = 'freqMovies.data'
data = np.loadtxt(fileFreq,delimiter =',')
X = data[:-1]
y = data[-1]

#filePerformance = 'performMovies.data'
#y = np.loadtxt(filePerformance,delimiter =',')

n,d = X.shape

#regularlize the data
mean = X.mean(axis=0)
std = X.std(axis=0)
X = (X - mean) / std

#predict
C = 0.01 #will do a gridsearch to tune this on testing data
model = svm.SVC(C = C, kernel='rbf', gamma=2) #why does this = 2
model.fit(X, y)

predictions = model.predict(X)
test_accuracy = metrics.accuracy_score(y, predictions)

