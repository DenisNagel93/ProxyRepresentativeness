import pandas as pd
import sys

#args
## [1] first table
## [2] second table
## [3] join attribute
## [4] joined table name

def computeJoin(df1,df2,a):
	return df1.set_index(a).join(df2.set_index(a),rsuffix='r',how='inner')

df1 = pd.read_csv(sys.argv[1])
df2 = pd.read_csv(sys.argv[2])

computeJoin(df1,df2,sys.argv[3]).to_csv(sys.argv[4])
