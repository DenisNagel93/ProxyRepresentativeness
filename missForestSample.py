import sklearn.neighbors._base
import sys
sys.modules['sklearn.neighbors.base'] = sklearn.neighbors._base

from missingpy import MissForest
import pandas as pd
import numpy as np
import os

# Arguments
## 1. Mode
## 2. Folder with imputation-files
## 3. Output-Folder

def singleRun(path):
	df = pd.read_csv(sys.argv[2] + path)
	df = df.drop(columns=['Location'])
	df['ParentLocation'] = df['ParentLocation'].map({"Africa": 0,"Americas": 1,"Eastern Mediterranean": 2,"Europe": 3,"South-East Asia": 4,"Western Pacific": 5})
	imputer = MissForest()
	imp_data = imputer.fit_transform(df)
	np.savetxt(sys.argv[3] + path, imp_data, delimiter=',')

def fullRun():
	for fn in os.listdir(sys.argv[2]):
		df = pd.read_csv(sys.argv[2] + fn)[["Location","ParentLocation","Period","FactValueNumeric"]]
		df = df.drop(columns=['Location'])
		df['ParentLocation'] = df['ParentLocation'].map({"Africa": 0,"Americas": 1,"Eastern Mediterranean": 2,"Europe": 3,"South-East Asia": 4,"Western Pacific": 5})
		print(df.columns)
		imputer = MissForest()
		imp_data = imputer.fit_transform(df)
		path = sys.argv[3]
		if not os.path.exists(path):
			os.makedirs(path)
		#imp_data = imp_data.insert(0,["ID","Location","ParentLocation","Period","FactValueNumeric"])
		np.savetxt(path + fn, imp_data, delimiter=',')

if (sys.argv[1] == 'Full'):
	fullRun()
else:
	singleRun(sys.argv[1])