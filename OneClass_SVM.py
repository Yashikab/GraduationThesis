import pandas as pd
import numpy as np
from sklearn.svm import OneClassSVM

#--import sample point set --#
dataset = pd.read_csv('dataset_dist5.csv')

#--set origin--#
origin = dataset.loc[0,:]

#--get set P --#
set_num = len(dataset)
set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)

#--set SVM--#
clf = OneClassSVM()
clf.fit(set_P)
