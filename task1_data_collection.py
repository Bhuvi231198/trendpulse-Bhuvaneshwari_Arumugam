import requests
import time
from datetime import datetime
import os
import json

# API URLs
top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
items_url = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Headers
headers = {"User-Agent": "TrendPulse/1.0"}

# Categories with keywords
categories = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"],
    "others": []  # fallback category
}

# Store results
collected_stories = []

# Count stories per category
category_counts = {category: 0 for category in categories}


# Fetch top story IDs
def fetch_story_ids():
    try:
        response = requests.get(top_stories_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()[:500]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching story IDs: {e}")
        return []


# Fetch individual story
def fetch_story(story_id):
    try:
        response = requests.get(items_url.format(story_id), headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


# Categorize story based on title
def categorize_story(title):
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category

    return None  # will go to "others"


def main():
    print("Fetching top stories...")
    story_ids = fetch_story_ids()

    if not story_ids:
        print("No stories fetched.")
        return

    print(f"Total story IDs fetched: {len(story_ids)}")

    for i, story_id in enumerate(story_ids):

        story = fetch_story(story_id)
        if not story:
            continue

        title = story.get("title", "")

        # Get category or assign "others"
        assigned_category = categorize_story(title)
        category = assigned_category if assigned_category else "others"

        # Collect only if category limit not reached
        if category_counts[category] < 25:
            story_data = {
                "post_id": story.get("id", ""),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", ""),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_stories.append(story_data)
            category_counts[category] += 1

        # Stop early if all categories are filled
        if all(count >= 25 for count in category_counts.values()):
            print("All categories filled. Stopping early.")
            break

        # Small delay every 100 requests (to be polite to API)
        if i % 100 == 0 and i != 0:
            time.sleep(2)

    # Create data folder
    os.makedirs("data", exist_ok=True)

    # File name with date
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    # Save to JSON
    with open(filename, "w") as file:
        json.dump(collected_stories, file, indent=4)

    print(f"\nCollected {len(collected_stories)} stories.")
    print(f"Saved to {filename}")
    print("Category distribution:", category_counts)


# Run main script
if __name__ == "__main__":
    main()