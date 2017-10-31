import pandas as pd

#--import sample point set --#
dataset = pd.read_csv('dataset_dist5.csv')

#--set origin--#
origin = dataset.loc[0,:]

#--get set P --#

set_P = pd.DataFrame(dataset.tail(len(dataset)-1),copy=True)
