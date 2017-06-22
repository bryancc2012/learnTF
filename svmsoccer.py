
import pandas as pd
from pandas import DataFrame as df
import numpy as np
from sklearn import preprocessing, cross_validation, svm, linear_model

def getwinlost(result):
    if result<0:
        resultwl=-1
    elif result == 0:
        resultwl=0
    else :
        resultwl=1
    return(resultwl)

gamedf=df.from_csv("gamedata.csv", header=None, index_col=0)

gamedatahead=("score1","score2","asias1","asias2","asiash","asiae1","asiae2","asiaeh","eurosw","eurosd","eurosl","euroew","euroed","euroel","euroswd","eurosdd","eurosld","euroewd","euroedd","euroeld")
gamedf.column= gamedatahead

print(len(gamedf))

gamedf=df.dropna(gamedf)

print(len(gamedf))


gamedf["result"]=gamedf[1]-gamedf[2]

gamedf["resultwl"]=gamedf["result"].apply(getwinlost)

gamedf["asiad1"]=((gamedf[6]-gamedf[3])/gamedf[3])
gamedf["asiad2"]=((gamedf[7]-gamedf[4])/gamedf[4])
gamedf["asiadh"]=((gamedf[8]-gamedf[5])/gamedf[5])
gamedf["eurodw"]=((gamedf[12]-gamedf[9])/gamedf[12])
gamedf["eurodd"]=((gamedf[13]-gamedf[10])/gamedf[13])
gamedf["eurodl"]=((gamedf[14]-gamedf[11])/gamedf[14])

gamedataai=gamedf[[6,7,8,12,13,14,"asiad1","asiad2","asiadh","eurodw","eurodd","eurodl","resultwl"]]

#gamedataai=gamedf[[12,13,14,"resultwl"]]

print(gamedataai.head(20))
print(gamedataai.tail(20))

gamedataai.dropna()

X = np.array(gamedataai.drop(["resultwl"],1))
y = np.array(gamedataai["resultwl"])

X= preprocessing.scale(X)

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf=linear_model.LogisticRegression()
clf.decision_function_shape = "ovr"
clf.fit(X_train, y_train)

score=clf.score(X_test, y_test)
print (score)
