import pandas as pd
import numpy as np

# CSV file from task 2
filepath = "data/trends_clean.csv"

def main():
    try:
        # Load csv file to pandas data frame
        df = pd.read_csv(filepath)
        print(f"{len(df)} rows are loaded from {filepath}")
    except Exception as ex:
        print(f"Error loading file : {ex}")
        return
        
    # Print first 5 rows
    first_5_rows = df.head(5)
    print("The first 5 rows: \n", first_5_rows)

    # Print shape of data frame
    shape = df.shape
    print("Shape of dataframe: ", shape)

    # Find Avg score and num_comments 
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print("Average score :", avg_score.__round__(2))
    print("Average comments :", avg_comments.__round__(2))

    # mean, median, and standard deviation of score
    print("\n...Numpy analysis...")
    score_values = df["score"].values

    mean_score = round(np.mean(score_values), 2) 
    median_score = round(np.median(score_values), 2)
    std_dev_scores = round(np.std(score_values), 2)

    print("Mean score is: ", mean_score)
    print("Median score is: ", median_score)
    print("Standard deviation is: ", std_dev_scores)

    # Highest and lowest scores
    max_score = df["score"].max()
    min_score = df["score"].min()

    print("Highest score is:", max_score)
    print("Lowest score is: ",min_score )

    # Category with maximum stories
    category_counts = df["category"].value_counts()
    top_categroy = category_counts.idxmax()

    print(f"Maximum stories in top category \"{top_categroy}\" is {category_counts.max()}")

    # Story title with maximum comments
    max_comments_story = df.loc[df["num_comments"].idxmax()]
    title_max = max_comments_story["title"]
    comments_max = max_comments_story["num_comments"]
    print(f"Maximum commented story is \"{title_max}\" with {comments_max} comments")

    # Adding new columns
    # Engagement column
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # Is_popular column
    df["is_popular"] = df["score"] > avg_score

    updated_file_path = "data/trends_analysed.csv"
    df.to_csv(updated_file_path, index=False)
    
    print(f"\nUpdated file shape is {df.shape}")
    print(f"Saved to {updated_file_path}")

if __name__ == "__main__":
    main()