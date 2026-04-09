import pandas as pd
import matplotlib.pyplot as plt
import os

# file path from task -3
filepath = "data/trends_analysed.csv"

def main():
    try:
        # Load csv file to pandas data frame
        df = pd.read_csv(filepath)
        print(f"{len(df)} rows are loaded from {filepath}")
    except Exception as ex:
        print(f"Error loading file : {ex}")
        return
    
    # Create outputs folder if doesn't exists
    os.makedirs("outputs", exist_ok=True)

    """---Chart-1:Horizontal bar chart---"""
    # Sorting and taking first 10 stories
    top_10 = df.sort_values(by="score" , ascending=False).head(10)

    # Shortening the title upto 50 characters
    top_10["short_title"] = top_10["title"].apply(lambda x:x[:50] + "..." if len(x) > 50 else x)

    # Set chart properties
    plt.figure()
    plt.barh(top_10["short_title"], top_10["score"])
    plt.xlabel("SCORE")
    plt.ylabel("STORY_TITLE")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()
    plt.savefig("outputs/chart1_top_stories.png")
    plt.show()

    """---Chart-2:Bar chart---"""
    # Getting category and their stories count
    category_counts = df["category"].value_counts()

    # Set chart properties
    colors = ["red", "blue", "green", "orange", "purple", "cyan"]
    plt.figure()
    plt.bar(category_counts.index, category_counts.values, color = colors)
    plt.xlabel("Category")
    plt.ylabel("Number of stories")
    plt.title("Story counts per category")
    plt.savefig("outputs/chart2_categories.png")
    plt.show()

    """---Chart-3:Scatter plot chart---"""

    # Set chart properties
    popular = df[df["is_popular"] == True]
    non_popular = df[df["is_popular"] == False]

    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label = "Popular")
    plt.scatter(non_popular["score"], non_popular["num_comments"], label = "Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Comments")
    plt.title("Score vs Comments")
    plt.legend()
    plt.savefig("outputs/chart3_scatter.png")
    plt.show()

    # Dashboard (BONUS)
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # Chart 1 in dashboard
    axs[0].barh(top_10["short_title"], top_10["score"])
    axs[0].set_title("Top Stories")
    axs[0].invert_yaxis()

    # Chart 2 in dashboard    
    axs[1].bar(category_counts.index, category_counts.values, color = colors)
    axs[1].set_title("Story counts per category")

    # Chart 3 in dashboard
    axs[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axs[2].scatter(non_popular["score"], non_popular["num_comments"], label="Not Popular")
    axs[2].set_title("Score vs Comments")
    axs[2].legend()

    plt.suptitle("TrendPulse Dashboard")
    plt.savefig("outputs/dashboard.png")
    plt.show()
    print("All charts saved in outputs/ folder")

if __name__ == "__main__":
    main()