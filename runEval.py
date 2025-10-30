import pandas as pd
import sys
import csv
import os
from pathlib import Path
from scipy.stats import kstest
from scipy.stats import energy_distance
from scipy.stats import pearsonr

# Arguments
## 1. Number Quantils/Clusters
## 2. Mode (Full,Run,Eval)

def joinData(lines):
	if not os.path.exists("JoinFiles/"):
		os.makedirs("JoinFiles/")
	sp1 = lines[0].split("-")
	sp2 = lines[1].split("-")
	central = sp1[0] + "-" + sp2[0] + "-" + sp1[1]
	outname = "JoinFiles/Join-" + central + ".csv"
	os.system("python joinDataFrames.py Data/" + lines[0] + " Data/" + lines[1] + " Location " + outname)

def createSamples(central):
	path = "Samples/" + central + "/"
	if not os.path.exists(path):
		os.makedirs(path)
	outname = path + "Sample-" + central
	os.system("python createSamples.py JoinFiles/Join-" + central + ".csv " + outname + " Full")

def counterSamples(central):
	path = "CounterSamples/" + central + "/"
	if not os.path.exists(path):
		os.makedirs(path)
	outname = path + "Sample-" + central
	os.system("python counterSamples.py JoinFiles/Join-" + central + ".csv " + outname + " Full")

def createSubgroups(central,n,mode):
	tpath = "JoinFiles/Join-" + central + ".csv"
	opath = "ModifiedSamples/" + central + "/"
	if not os.path.exists(opath):
		os.makedirs(opath)
	for fn in os.listdir("Samples/" + central + "/"):		
		spath = "\"Samples/" + central + "/" + fn + "\""
		outname = "\"" + opath + "Mod" + fn + "\""
		os.system("python createSubgroups.py " + tpath + " " + spath + " FactValueNumericr " + str(n) + " " + outname + " " + mode)

def createDynSubgroups(central):
	path = "ModifiedSamples/" + central + "/"
	if not os.path.exists(path):
		os.makedirs(path)
	outname = path + "ModSample-" + central
	os.system("python createDynamicSubgroups.py JoinFiles/Join-" + central + ".csv " + outname + " FactValueNumericr " + central)

def createRandomSamples(central,n):
	path = "Samples/" + central + "/"
	if not os.path.exists(path):
		os.makedirs(path)
	outname = path + "Sample-" + central
	for i in range(0,n): 
		os.system("python randomSample.py JoinFiles/Join-" + central + ".csv " + outname + "-Z50_" + str(i) + ".csv " + str(50))
	
def imputation(s,i,o):
	os.system("python prepareImpSamples.py " + s + " " + i)
	os.system("python missForestSample.py Full " + i + " " + o)

def ksTest(sf,tf,a):
	sdf = pd.read_csv(sf)
	tdf = pd.read_csv(tf)

	return kstest(sdf[a],tdf[a])

def ksTest2(sf,tf,a,b):
	sdf = pd.read_csv(sf)
	tdf = pd.read_csv(tf)

	return kstest(sdf[a],tdf[b])

def gatherResults(central):
	if not os.path.exists("Results/"):
		os.makedirs("Results/")
	with open("Results/Results-" + central + ".txt", "w") as f:
		cs = central.split("-")
		origPath = "Data/" + cs[0] + "-" + cs[2] + "-Data.csv"
		ctrPath = "CounterSamples/" + central + "/"
		spath = "Samples/" + central + "/"
		tpath = "JoinFiles/Join-" + central + ".csv"
		f.write("Region, p-Value Sample, p-Value Modified, p-Value Sample (Orig.), p-Value Modified (Orig.), Rep.Score, Imputation Delta, Mean (Sample))")
		f.write("\n")
		tpS = 0
		tpM = 0
		total = 0
		impP = 0
		impO = 0
		repScore = 0
		distSim = 0
		enerDist = 0
		sme = 0
		cme = 0

		pcdf = pd.read_csv(tpath)
		pcdf.dropna(subset=["FactValueNumeric","FactValueNumericr"],inplace=True)
		pScore = pearsonr(pcdf["FactValueNumeric"],pcdf["FactValueNumericr"])
			
		for fn in os.listdir(spath):
			sp = fn.split("-")
			reg = sp[4]
			if (len(sp)>5):
				for i in range(5,len(sp)):
					reg = reg + "-" + sp[i]
			
			rS = ksTest(spath + fn,tpath,"FactValueNumeric").pvalue
							
			sm = pd.read_csv(spath + fn)["FactValueNumeric"].mean()
		
			pvS = ksTest(spath + fn,tpath, "FactValueNumericr").pvalue
			pvM = ksTest("Modified" + spath + "Mod" + fn,tpath, "FactValueNumericr").pvalue
			pvSO = ksTest(spath + fn,tpath, "FactValueNumeric").pvalue
			pvMO = ksTest("Modified" + spath + "Mod" + fn,tpath, "FactValueNumeric").pvalue
						
			idf = pd.read_csv("ImputedSamples/" + central + "/" + fn)
			gtdf = pd.read_csv(tpath)
			
			f.write(reg.split(".")[0] + ", ")
			f.write(str(pvS) + ", ")
			f.write(str(pvM) + ", ")
			f.write(str(pvSO) + ", ")
			f.write(str(pvMO) + ", ")
			f.write(str(rS) + ", ")
			f.write(str(abs(idf.iloc[:,2].mean() - gtdf['FactValueNumeric'].mean())) + ", ")
			f.write(str(sm))
			f.write("\n")

			total = total + 1
			if ((pvS >= 0.05 and pvSO >= 0.05) or (pvS < 0.05 and pvSO < 0.05)):
					tpS = tpS + 1
			if ((pvM >= 0.05 and pvMO >= 0.05) or (pvM < 0.05 and pvMO < 0.05)):
					tpM = tpM + 1
			if (pvM >= pvS):
				impP = impP + 1
			if (pvMO >= pvSO):
				impO = impO + 1
			repScore = repScore + rS
			sme = sme + sm

		f.write("\n")
		f.write("Proxy-Score (PCC): " + str(pScore))
		f.write("\n")
		f.write("Proxy-Score Sample: " + str(tpS / total))
		f.write("\n")
		f.write("Proxy-Score Modified Sample: " + str(tpM / total))
		f.write("\n")
		f.write("Proxy-Score Total: " + str((tpS + tpM) / (2*total)))
		f.write("\n")
		f.write("\n")
		f.write("Modified is Improvement (Proxy): " + str(impP / total))
		f.write("\n")
		f.write("Modified is Improvement (Original): " + str(impO / total))
		f.write("\n")
		f.write("\n")
		f.write("Representativeness of Initial Sample: " + str(repScore / total))
		f.write("\n")
		f.write("\n")
		f.write("Avg. Mean (Sample): " + str(sme / total))
		
def writeRaw(csvFile):
	if not os.path.exists("Results/"):
		os.makedirs("Results/")

	with open("Results/Raw-Complete.csv", "w") as f:

		f.write("Query, Region, Mean (Baseline), Mean (MissForest), Mean (ProxyRep), Mean (Hybrid)")
		f.write("\n")

		for lines in csvFile:
			sp1 = lines[0].split("-")
			sp2 = lines[1].split("-")
			central = sp1[0] + "-" + sp2[0] + "-" + sp1[1]

			cs = central.split("-")
			origPath = "Data/" + cs[0] + "-" + cs[2] + "-Data.csv"
			spath = "Samples/" + central + "/"
			tpath = "JoinFiles/Join-" + central + ".csv"
		

			for fn in os.listdir(spath):
				sp = fn.split("-")
				reg = sp[4]
				if (len(sp)>5):
					for i in range(5,len(sp)):
						reg = reg + "-" + sp[i]
											
				idf = pd.read_csv("ImputedSamples/" + central + "/" + fn)
				midf = idf
				#mdf = pd.read_csv("ImputedSamples/" + cs[0] + "-" + cs[2] + "/" + cs[0] + "-" + cs[2] + "-" + reg)
				mdf = pd.read_csv("ModifiedSamples/" + central + "/Mod" + fn)
				gtdf = pd.read_csv(tpath)
			
				gmean = gtdf['FactValueNumeric'].mean()
		
				pvS = ksTest(spath + fn,tpath, "FactValueNumericr").pvalue
				pvM = ksTest("ModifiedSamples/" + central + "/Mod" + fn,tpath, "FactValueNumericr").pvalue
				#pvS = ksTest(spath + fn,tpath, "FactValueNumericr").statistic
				#pvM = ksTest("ModifiedSamples/" + central + "/Mod" + fn,tpath, "FactValueNumericr").statistic

				mdf = pd.read_csv(spath + fn)
				max = pvS
				if (pvM >= pvS):
					mdf = pd.read_csv("ModifiedSamples/" + central + "/Mod" + fn)
					max = pvM
					midf = pd.read_csv("ModImputedSamples/" + central + "/Mod" + fn)
				
				f.write(central + ", ")
				f.write(reg.split(".")[0] + ", ")
				f.write(str(abs(pd.read_csv(spath + fn)['FactValueNumeric'].mean() - gmean)/gmean) + ", ")
				f.write(str(abs(idf.iloc[:,2].mean() - gmean)/gmean) + ", ")
				if (pvS >= 0.05):
					f.write(str(abs(pd.read_csv(spath + fn)['FactValueNumeric'].mean() - gmean)/gmean) + ", ")
					f.write(str(abs(idf.iloc[:,2].mean() - gmean)/gmean))
				else:
					f.write(str(abs(mdf['FactValueNumeric'].mean() - gmean)/gmean) + ", ")
					f.write(str(abs(midf.iloc[:,2].mean() - gmean)/gmean))
				f.write("\n")


def writeImpRaw(csvFile):
	if not os.path.exists("Results/"):
		os.makedirs("Results/")
	
	with open("Results/ImpRaw-Complete.csv", "w") as f:
		
		f.write("Query, Region, Mean (Baseline), Mean (MissForest), Mean (ProxyRep), Mean (Hybrid)")
		f.write("\n")

		for lines in csvFile:
			sp1 = lines[0].split("-")
			sp2 = lines[1].split("-")
			central = sp1[0] + "-" + sp2[0] + "-" + sp1[1]

			cs = central.split("-")
			origPath = "Data/" + cs[0] + "-" + cs[2] + "-Data.csv"
			spath = "Samples/" + central + "/"
			tpath = "JoinFiles/Join-" + central + ".csv"
			

			for fn in os.listdir(spath):
				sp = fn.split("-")
				reg = sp[4]
				if (len(sp)>5):
					for i in range(5,len(sp)):
						reg = reg + "-" + sp[i]
											
				idf = pd.read_csv("ImputedSamples/" + central + "/" + fn)
				midf = idf
				#mdf = pd.read_csv("ImputedSamples/" + cs[0] + "-" + cs[2] + "/" + cs[0] + "-" + cs[2] + "-" + reg)
				mdf = pd.read_csv("ModifiedSamples/" + central + "/Mod" + fn)
				gtdf = pd.read_csv(tpath)
			
				gmean = gtdf['FactValueNumeric'].quantile(0.25)
		
				pvS = ksTest(spath + fn,tpath, "FactValueNumericr").pvalue
				pvM = ksTest("ModifiedSamples/" + central + "/Mod" + fn,tpath, "FactValueNumericr").pvalue
				#pvS = ksTest(spath + fn,tpath, "FactValueNumericr").statistic
				#pvM = ksTest("ModifiedSamples/" + central + "/Mod" + fn,tpath, "FactValueNumericr").statistic

				mdf = pd.read_csv(spath + fn)
				max = pvS
				if (pvM >= pvS):
					mdf = pd.read_csv("ModifiedSamples/" + central + "/Mod" + fn)
					max = pvM
					midf = pd.read_csv("ModImputedSamples/" + central + "/Mod" + fn)

			
				if (pvS < 0.05):
					f.write(central + ", ")
					f.write(reg.split(".")[0] + ", ")
					f.write(str(abs(pd.read_csv(spath + fn)['FactValueNumeric'].quantile(0.25) - gmean)/gmean) + ", ")
					f.write(str(abs(idf.iloc[:,2].quantile(0.25) - gmean)/gmean) + ", ")
					f.write(str(abs(mdf['FactValueNumeric'].quantile(0.25) - gmean)/gmean) + ", ")
					f.write(str(abs(midf.iloc[:,2].quantile(0.25) - gmean)/gmean))
					f.write("\n")
		


with open('settings.csv', mode='r') as file:
	csvFile = csv.reader(file)
	if (sys.argv[2] == "Eval" or sys.argv[2] == "Full"):
		#writeRaw(csvFile)
		writeImpRaw(csvFile)
	for lines in csvFile:
		sp1 = lines[0].split("-")
		sp2 = lines[1].split("-")
		central = sp1[0] + "-" + sp2[0] + "-" + sp1[1]
		if (sys.argv[2] == "Prepare"):
			joinData(lines)
			createSamples(central)
			#createRandomSamples(central,21)
			createSubgroups(central,sys.argv[1],"Cluster")
		if (sys.argv[2] == "Impute"):
			imputation("Samples/" + central + "/","ImputationSamples/" + central + "/","ImputedSamples/" + central + "/")
			imputation("ModifiedSamples/" + central + "/","ModImputationSamples/" + central + "/","ModImputedSamples/" + central + "/")
		#if (sys.argv[2] == "Eval"):
			#gatherResults(central)
		if (sys.argv[2] == "Full"):
			joinData(lines)
			createSamples(central)
			#createRandomSamples(central,21)
			createSubgroups(central,sys.argv[1],"Cluster")
			imputation("Samples/" + central + "/","ImputationSamples/" + central + "/","ImputedSamples/" + central + "/")
			imputation("ModifiedSamples/" + central + "/","ModImputationSamples/" + central + "/","ModImputedSamples/" + central + "/")
			#gatherResults(central)
	
