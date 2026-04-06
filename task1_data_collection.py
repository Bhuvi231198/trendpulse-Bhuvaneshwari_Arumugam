import requests
import time
from datetime import datetime
import os
import json

# Saving inputs to variables
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
items_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"
headers = {"User-Agent": "TrendPulse/1.0"}

catagories = {
    "technology":["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews":["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports":["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science":["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment":["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
}

# To fetch top 500 story IDs as List
def fetch_story_IDs():
    try:
        response = requests.get(top_stories_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as ex:
        print(f"Error fetching top 500 stories: {ex}")
        return []

# To fetch each story by story id
def fetch_story(story_id):
    try:        
        response = requests.get(items_url.format(story_id), headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        print(f"Error fetching story {story_id} : {ex}")
        return None

# To catagories stories by title
def catagorize_story(title):
    if not title:
        return None
    
    title_lower = title.lower()
    for category, keywords in catagories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    
    return None

# Global variables to store collected stories and their count(to stop at 25)
collected_stories = []
category_counts = {category: 0 for category in catagories}

# Define main function
def main():
    story_ids = fetch_story_IDs()
    print(len(story_ids))

    if not story_ids:
        print("No stories fetched.")
        return
    
    # Loop thru each story IDs
    for i,story_id in enumerate(story_ids):
        if not story_id:
            continue

        story = fetch_story(story_id)
        if not story:
            continue

        title = story.get("title", "")
        assigned_category = catagorize_story(title)
        if not assigned_category:
            continue

        # Loop thru each category
        for category in catagories:
            if category is not assigned_category:
                story_data = {
                "post_id":story.get("id", ""),
                "title": story.get("title", ""),
                "category": "Others",
                "score":story.get("score", ""),
                "num_comments":story.get("descendants", ""),
                "author": story.get("by",""),
                "Collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
                continue

            # Stop if collected 25 stories in current category
            if category_counts[assigned_category] >= 25:
                continue
            
            story_data = {
                "post_id":story.get("id", ""),
                "title": story.get("title", ""),
                "category": assigned_category,
                "score":story.get("score", ""),
                "num_comments":story.get("descendants", ""),
                "author": story.get("by",""),
                "Collected_at":datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_stories.append(story_data)
            category_counts[assigned_category]+=1

            # Sleep after each 100 stories looped
            if i%100 == 0 and i != 0:
                time.sleep(2)
    
    # Create data directory if doesn't exists
    os.makedirs("data", exist_ok=True)

    # Define a filename variable with date and time
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save collected stories to JSON file
    with open(filename, "w") as file:
        json.dump(collected_stories, file, indent=4)
    
    print(f"Collected {len(collected_stories)} and Saved to {filename}")
    print("Stories by category", category_counts)

main()