from sklearn.datasets import load_iris
from sklearn.datasets import load_digits

data = load_iris()
data2 = load_digits()
X,y = data
X1,y1 = data2
print(X.shape)
print(y.shape)

print(X1.shape)
print(y1.shape)