#pip install scikit-learn
from sklearn.linear_model import LinearRegression

X=[[1],[2],[3],[4],[5]]
y=[5,8,12,15,16]

modelo=LinearRegression()
modelo.fit(X,y)

print(modelo.predict([[6]]))

