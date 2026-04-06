import pandas as pd
import os

# File from task-1
filepath = "data/trends_20260406.json"

def main():
    try:
        # 1-Load json file to data frame
        df = pd.read_json(filepath)
        print(f"Loaded {len(df)} stories from {filepath}")
    except Exception as ex:
        print(f"Error loading file: {ex}")
        return
    
    # 2-Clean data
    print(f"Initial row count is: {len(df)}")

    # Remove duplicates in post id
    df_new = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicate post ids : {len(df_new)}")

    # Drop the row if post_id, title, or score values are missing
    df_new = df_new.dropna(subset=["post_id", "title", "score"])
    print(f"After removing missing rows : {len(df_new)}")

    # Converting score and num_comments column as integer
    df_new["score"] = df_new["score"].astype(int)
    df_new["num_comments"] = df_new["num_comments"].fillna(0).astype(int)

    # Remove low quality stories where score is less than 5
    df_new = df_new[df_new["score"] > 5]
    print(f"After removing low quality stories : {len(df_new)}")  

    # Strip extra white spaces from title column
    df_new["title"] = df_new["title"].str.strip()

    # Create data directory if not exists
    os.makedirs("data", exist_ok=True)

    # Create .CSV files
    output_file = f"data/trends_clean.csv"
    df_new.to_csv(output_file, index=False)

    print(f"Saved {len(df_new)} stories to {output_file}")

    print("\nSummary : Stories per category")
    print("\nStories per category:")
    print(df_new["category"].value_counts())

if __name__ == "__main__":
    main()