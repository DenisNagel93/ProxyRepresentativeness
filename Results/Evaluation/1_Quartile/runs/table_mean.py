import pandas as pd
import glob

def main():
    files = glob.glob("*.csv")
    if not files:
        print("Keine CSV-Dateien gefunden!")
        return

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        
        # Spaltennamen säubern
        df.columns = df.columns.str.strip().str.replace("\ufeff", "", regex=True)

        # sicherstellen, dass Query/Region existieren
        if "Query" not in df.columns or "Region" not in df.columns:
            print(f"File {f}: Column missing:", df.columns.tolist())
            return

        dfs.append(df)

    combined = pd.concat(dfs, ignore_index=True)

    # numerische Spalten casten
    numeric_cols = combined.columns.difference(["Query", "Region"])
    combined[numeric_cols] = combined[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Mittelwerte bilden
    result = combined.groupby(["Query", "Region"], as_index=False).mean()

    result.to_csv("combined_means.csv", index=False)
    print("Done. created combined_means.csv")

if __name__ == "__main__":
    main()

