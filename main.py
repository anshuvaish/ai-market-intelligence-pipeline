# Import the functions we built in the other files
from extract import fetch_unstructured_data
from transform import extract_structured_data
from load import push_to_google_sheets
import pandas as pd
import time

def run_pipeline():
    print("--- Starting Daily AI Data Pipeline ---")
    
    # 1. Extract
    target_url = "https://techcrunch.com/feed/" 
    raw_df = fetch_unstructured_data(target_url)
    
    # 2. Transform (Using just 3 rows to stay safely under your current quota)
    df_test = raw_df.head(3).copy()
    df_test['published_date'] = pd.to_datetime(df_test['published_date'], utc=True).dt.strftime('%Y-%m-%d')
    
    ai_results = []
    for index, row in df_test.iterrows():
        print(f"Enriching article {index + 1}...")
        result = extract_structured_data(row['summary'])
        ai_results.append(result)
        time.sleep(3) # Extra padding for the rate limit
        
    ai_df = pd.DataFrame(ai_results)
    enriched_df = pd.concat([df_test.reset_index(drop=True), ai_df], axis=1)
    enriched_df.to_csv("daily_enriched_data.csv", index=False)
    
    # 3. Load
    target_spreadsheet = "AI_News_Enrichment_Pipeline"
    push_to_google_sheets("daily_enriched_data.csv", target_spreadsheet, "Raw Data")
    
    print("--- Pipeline Complete ---")

if __name__ == "__main__":
    run_pipeline()