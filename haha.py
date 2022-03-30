import sklearn.preprocessing as preprocessing

X = [[1.], [-1.],  [2.]]

s = preprocessing.MinMaxScaler()

print(s.fit_transform(X))