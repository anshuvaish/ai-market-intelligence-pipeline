import feedparser
import pandas as pd

def fetch_unstructured_data(rss_url):
    print(f"Fetching data from: {rss_url}...")
    
    # 1. Parse the live feed
    feed = feedparser.parse(rss_url)
    
    extracted_data = []
    
    # 2. Loop through each article in the feed
    for entry in feed.entries:
        # Grab the messy, unstructured text elements
        article_data = {
            "title": entry.get("title", ""),
            "summary": entry.get("summary", ""),
            "link": entry.get("link", ""),
            "published_date": entry.get("published", "")
        }
        extracted_data.append(article_data)
        
    # 3. Convert the raw list into a structured Pandas DataFrame
    df = pd.DataFrame(extracted_data)
    return df

if __name__ == "__main__":
    # We are using a generic tech news RSS feed as our messy data source
    target_url = "https://techcrunch.com/feed/" 
    
    raw_dataframe = fetch_unstructured_data(target_url)
    
    print("\nExtraction Complete! Here is a preview of the raw data:")
    print(raw_dataframe[['title', 'published_date']].head())
    
    # Save it to a CSV to review the raw, uncleaned text
    raw_dataframe.to_csv("raw_data.csv", index=False)
    print("\nSaved to raw_data.csv")