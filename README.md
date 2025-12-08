# ProxyRepresentativeness

The goal of this work is to assess the **representativeness** of incomplete tabular datasets using **proxy attributes** and, if necessary, generate **representative modified samples** from the available data.
Approach:

1. Identify a relevant witness table for a query
2. Join it with a proxy attribute from a more complete dataset
3. Creates samples (initial and modified)
4. Evaluates representativeness statistically (KS-tests, Pearson correlation)
5. Performs missing-value imputation
6. Quantifies the quality of each resulting sample and imputed dataset

The entire pipeline is orchestrated via **`runEval.py`**.

---


# Datasets

We use real-world data from two WHO repositories:

### ● Global Health Observatory (GHO)

[https://www.who.int/data/gho](https://www.who.int/data/gho)

### ● Health Equity Assessment Toolkit (HEAT Plus)

[https://www.who.int/data/inequality-monitor/assessment_toolkit](https://www.who.int/data/inequality-monitor/assessment_toolkit)


---

# Queries

The evaluation uses **13 narrative claims from WHO Data Stories**:

[https://www.who.int/data/stories](https://www.who.int/data/stories)


---

# Evaluation Pipeline

The processing pipeline is done as follows:

### **1. Join witness and proxy tables**

Using `joinDataFrames.py`.

### **2. Create initial samples**

Using `createSamples.py`.

### **3. Create modified samples (cluster or quantile-based)**

Using `createSubgroups.py`.

### **4. Generate random samples (optional)**

Using `randomSample.py`.

### **5. Impute missing values (MissForest)**

Using `prepareImpSamples.py` and `missForestSample.py`.

### **6. Compute representativeness and performance metrics**

* KS-tests on numeric indicator distributions
* Mean errors relative to ground truth
* Proxy-score improvements
* Imputation performance
  Output stored in `Results/`.

The entire pipeline is controlled by **`runEval.py`**.

---

# Using `runEval.py`

```
python3 runEval.py <#clusters/quantiles> <mode>
```

### Arguments

| Argument                | Meaning                                                         |
| ----------------------- | --------------------------------------------------------------- |
| `<#clusters/quantiles>` | Number of clusters/quantiles for subgrouping (Paper uses **4**) |
| `<mode>`                | `Prepare`, `Impute`, `Eval`, or `Full`                          |

Requires the data sets in the **Data folder** as well as the **settings.csv** file, which specifies each witness and proxy table combination.

---

## Modes in Detail

### **Prepare**

```
python3 runEval.py 4 Prepare
```

Joins all witnesses with their respective proxy table as assigned in settings.csv:

```
JoinFiles/
```

Creates initial samples:

```
Samples/<central>/
```

Generates cluster- or quantile-based modified samples:

```
ModifiedSamples/<central>/
```

---

### **Impute**

```
python3 runEval.py 4 Impute
```

Prepares data sets for imputation:

```
ImputationSamples/<central>/
ModImputationSamples/<central>/
```

Runs MissForest imputation and generates imputed data sets:

```
ImputedSamples/<central>/
ModImputedSamples/<central>/
```

---

### **Eval**

```
python3 runEval.py 4 Eval
```

Writes global metrics:

```
Results/ImpRaw-Complete.csv
```

Content includes:

* Mean deviation of Baseline
* Mean deviation of MissForest
* Mean deviation of Proxy-based representative sample
* Mean deviation of Hybrid (Proxy + MissForest)


---

### **Full**

```
python3 runEval.py 4 Full
```

Runs the complete sequence:

1. Create modified samples
2. Impute samples and modified samples
3. Output final evaluation CSVs


---

# ***Experiments Are Run 10× (Mean Values)***

As described in the paper (Sec. IV):

> **All experiments — including sampling, subgroup generation, and imputation — were executed 10 independent times. All reported results in the paper are the *mean over these 10 runs*.**


To reproduce the published results, you must run `runEval.py` **10 times** and average the outputs.

Calculate:

* Average representativeness (KS)
* Mean deviation
* Proxy-score
* Imputation performance

The averaged metrics match the numbers presented in the paper.

---

# Dependencies
```
pandas>=1.4
numpy>=1.20
scipy>=1.7
scikit-learn>=1.0
missingpy>=0.2.0
tqdm>=4.60
python-dateutil>=2.8
```


