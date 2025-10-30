import pandas as pd
import sys
from sklearn.cluster import KMeans
import kmeans1d

#Arguments
## 1. Target-File
## 2. Sample-File
## 3. Proxy-Attribute
## 4. Number Quantils/Clusters
## 5. Output-File
## 6. Mode

def regionToStr(l):
	s = l[0]
	for k in range(1,len(l)):
		s = s + "+" + l[k]
	return s

def getMin(qdf,df):
	min = len(df.index)
	for x in qdf:
		l = len(x.index)
		if l < min:
			if l > 4:
				min = l
			else:
				min = 5
	return min
	
def buildSample(groups,df,smdf):
	qdf = []

	for x in groups:
		q_sample = x.loc[x['Location'].isin(smdf['Location'])]
		qdf.append(q_sample)

	min = getMin(qdf,df)

	sdf = []

	for x in qdf:
		s = x
		if len(x.index) >= min:
			s = x.sample(n=min)
		sdf.append(s)

	sample = pd.concat(sdf) 
	sample.to_csv(sys.argv[5])

def removeOutliers(df,a):
	tdf = df
	q1 = tdf[a].quantile(0.25)
	q3 = tdf[a].quantile(0.75)
	iqr = q3-q1

	ub = q3 + 1.5 * iqr
	lb = q1 - 1.5 * iqr

	udf = tdf.loc[tdf[a] >= ub]
	ldf = tdf.loc[tdf[a] <= lb]

	tdf = tdf.loc[~tdf['Location'].isin(udf['Location'])]
	tdf = tdf.loc[~tdf['Location'].isin(ldf['Location'])]	

	return tdf

def determineClusters(df,a,n):
	clusters, centroids = kmeans1d.cluster(df[a],n)
	df['Cluster'] = clusters

	qdf = []

	for i in range(0,n):
		sdf = df.loc[df['Cluster'] == i]
		sdf = sdf.drop('Cluster', axis=1)
		qdf.append([i,len(sdf.index)/len(df.index),sdf])

	return qdf

def buildClusterSample(groups,df,smdf):
	qdf = []

	sampleSize = len(smdf.index)
	for x in groups:
		xdf = x[2]
		q_sample = xdf.loc[xdf['Location'].isin(smdf['Location'])]
		qdf.append([x[0],len(q_sample.index)/sampleSize,q_sample])

	sdf = []

	for i in range(0,len(qdf)):
		cdf = qdf[i][2]
		while qdf[i][1] > groups[i][1] and len(cdf.index) > 1:
			cdf = cdf.sample(n=len(cdf.index)-1)
			sampleSize = sampleSize - 1
			qdf[i][2] = cdf
			qdf[i][1] = len(cdf)/sampleSize
		sdf.append(cdf)

	sample = pd.concat(sdf) 
	sample.to_csv(sys.argv[5])

def determineQuantils(df,a,n):
	d = 1.0 / float(n) 	
	c = 0.0		
	cn = c + d
	r = 0		
	quantils = []

	while cn <= 1:
		r = r + 1		
		q = df
		if (r == 1):
			q = df.loc[df[a] < df[a].quantile(cn)]
		else:
			if (cn + d <= 1):
				q = df.loc[(df[a] >= df[a].quantile(c)) & (df[a] < df[a].quantile(cn))]
			else:
				q = df.loc[df[a] >= df[a].quantile(c)]
		c = cn
		cn = c + d
		quantils.append(q)	

	return quantils
	

df = pd.read_csv(sys.argv[1])
a = sys.argv[3]

df = removeOutliers(df,a)

if (sys.argv[6] == 'Quantil'):
	quantils = determineQuantils(df,a,sys.argv[4])
	buildSample(quantils,df,pd.read_csv(sys.argv[2]))
if (sys.argv[6] == 'Cluster'):
	clusters = determineClusters(df,a,int(sys.argv[4]))
	buildClusterSample(clusters,df,pd.read_csv(sys.argv[2]))


