import pandas as pd
import glob

"""
Load all CSV files in the current folder, checks they contain Query and Region columns, cleans and merges them, converts numeric columns, and then computes the mean values grouped by Query and Region, saving the result as combined_means.csv.

"""

def main():
    files = glob.glob("*.csv")
    if not files:
        print("No csv file found")
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        
        # get clean column names
        df.columns = df.columns.str.strip().str.replace("\ufeff", "", regex=True)

        # make sure that Query/Region exist
        if "Query" not in df.columns or "Region" not in df.columns:
            print(f"File {f}: Column missing:", df.columns.tolist())
            return

        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)

    # type cast
    numeric_cols = combined.columns.difference(["Query", "Region"])
    combined[numeric_cols] = combined[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # calculate mean
    result = combined.groupby(["Query", "Region"], as_index=False).mean()

    result.to_csv("combined_means.csv", index=False)
    print("Done. created combined_means.csv")

if __name__ == "__main__":
    main()

