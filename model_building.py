# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 07:38:24 2020

@author: Gehlot Pratik
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('eda_data.csv')


# choose relevant columns
df.columns

df_model = df[['avg_salary','Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'num_comp', 'hourly', 'employer_provided', 
               'job_state' , 'same_state' , 'age', 'python_yn', 'spark', 'aws', 'excel', 'job_simp', 'seniority' , 'desc_len']]


# get dummy variables (for categorical variable)
df_dum = pd.get_dummies(df_model)

# train test split
from sklearn.model_selection import train_test_split
X = df_dum.drop('avg_salary', axis = 1)
y = df_dum.avg_salary.values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# multiple linear regression
import statsmodels.api as sm
X_sm = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()

from sklearn.linear_model import LinearRegression ,Lasso
from sklearn.model_selection import cross_val_score

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm , X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

# lasso regression (sparse)
lm_l = Lasso(alpha = 0.13)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l , X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))

alpha = []
error = []
for i in range(1,100):
    alpha.append(i/100)
    lml = Lasso(alpha = (i/100))
    error.append(np.mean(cross_val_score(lml , X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3)))

plt.plot(alpha, error)
err = tuple(zip(alpha,error))
df_err = pd.DataFrame(err , columns = ['alpha', 'error'])
df_err[df_err.error == max(df_err.error)]


# Random forest
from sklearn.ensemble import RandomForestRegressor 
rf = RandomForestRegressor()
rf.fit(X_train, y_train)
np.mean(cross_val_score(rf , X_train, y_train, scoring = 'neg_mean_absolute_error', cv = 3))


# tune models GridSearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10,300,10), 'criterion':('mse','mae'), 'max_features':('auto','sqrt','log2')}

gs = GridSearchCV(rf,parameters,scoring='neg_mean_absolute_error',cv=3)
gs.fit(X_train,y_train)

gs.best_score_
gs.best_estimator_


# test ensembles
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)    
tpred_rf = rf.predict(X_test)   


from sklearn.metrics import mean_absolute_error
print(mean_absolute_error(y_test, tpred_lm))
print(mean_absolute_error(y_test, tpred_lml))
print(mean_absolute_error(y_test, tpred_rf))

mean_absolute_error(y_test, (tpred_lml + tpred_rf)/2)



















