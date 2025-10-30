import pandas as pd
import sys

# Arguments
## 1. csv-file
## 2. output file
## 3. #records

df = pd.read_csv(sys.argv[1])
sample = df.sample(n=int(sys.argv[3]))

sample.to_csv(sys.argv[2])