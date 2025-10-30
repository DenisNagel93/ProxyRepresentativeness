import os
import pandas as pd
import sys

# Arguments
## 1. Folder with Samples
## 2. Output Folder

for fn in os.listdir(sys.argv[1]):
	df = pd.read_csv(sys.argv[1] + fn)
	s = fn.split("-")
	jdf = pd.read_csv("JoinFiles/Join-" + s[1] + "-" + s[2] + "-" + s[3] + ".csv")
	cdf = jdf.loc[jdf['Location'].isin(df['Location'])]
	rdf = jdf.loc[~jdf['Location'].isin(df['Location'])]
	rdf['FactValueNumeric'] = ""
	rslt_df = pd.concat([cdf,rdf])
	if not os.path.exists(sys.argv[2]):
		os.makedirs(sys.argv[2])
	rslt_df.to_csv(sys.argv[2] + fn)