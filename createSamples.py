import pandas as pd
import sys
import re

# Arguments
## 1. csv-file
## 2. output-file
## 3. context (comma-separated list)

def select_rows(df,a,ar):
	rslt_df = df.loc[df[a].isin(ar)]
	t = ar[0]
	if (len(ar)>1):
		for c in range(1,len(ar)):
			t = t + "+" + ar[c]
	rslt_df.to_csv(sys.argv[2] + '-' + t + '.csv')

def partitionCSV(df,a,ar):
	for x in ar:
		select_rows(df,a,x)

def createSample(df,a,ar):
	rslt_df = df.loc[df[a].isin(ar)]
	rslt_df.to_csv(sys.argv[2])

regions = [["Africa"], ["Americas"], ["Eastern Mediterranean"], ["Europe"], ["South-East Asia"], ["Western Pacific"], ["Africa", "Americas"], ["Africa", "Eastern Mediterranean"], ["Africa", "Europe"], ["Africa", "South-East Asia"], ["Africa", "Western Pacific"], ["Americas", "Eastern Mediterranean"], ["Americas", "Europe"], ["Americas", "South-East Asia"], ["Americas", "Western Pacific"], ["Eastern Mediterranean", "Europe"], ["Eastern Mediterranean", "South-East Asia"], ["Eastern Mediterranean", "Western Pacific"], ["Europe", "South-East Asia"], ["Europe", "Western Pacific"], ["South-East Asia", "Western Pacific"]]

df = pd.read_csv(sys.argv[1])

if (sys.argv[3]=='Full'):
	partitionCSV(df,'ParentLocation',regions)
else:
	sp = re.split(r',', sys.argv[3])
	createSample(df,'ParentLocation',sp)