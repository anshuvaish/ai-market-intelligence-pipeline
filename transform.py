import pandas as pd
from google import genai
from google.genai import types
import json
import time
import os # NEW: Import the OS library to read hidden environment variables

# NEW: Fetch the hidden key from the cloud server
api_key = os.environ.get("GEMINI_API_KEY")

# 1. Initialize the new API Client securely
client = genai.Client(api_key=api_key)

def extract_structured_data(text):
    """Passes raw text to the LLM and returns structured JSON."""
    
    prompt = f"""
    You are a strict data extraction pipeline. Analyze the following text and extract the requested entities.
    
    Structure required:
    {{
        "category": "One word category (e.g., AI, Hardware, Finance, Startup, Unknown)",
        "sentiment": "Positive, Negative, or Neutral",
        "key_entities": "Up to 3 main companies, products, or people mentioned"
    }}
    
    Text to analyze:
    {text}
    """
    
    try:
        # 2. Use the new models.generate_content method and force JSON output
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # 3. Parse the guaranteed JSON string into a Python dictionary
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return {"category": "Error", "sentiment": "Error", "key_entities": "Error"}

if __name__ == "__main__":
    # 4. Load the messy data
    df = pd.read_csv("raw_data.csv")
    
    # NEW FIX: Clean the date format to YYYY-MM-DD
    df['published_date'] = pd.to_datetime(df['published_date'], utc=True).dt.strftime('%Y-%m-%d')
    
    # NEW FIX: Process all rows, not just the first 5
    df_test = df.copy() 
    
    print("Sending data to the AI model for enrichment...")
    # ... the rest of your code remains exactly the same ...
    
    # 5. Apply the AI extraction to each row's summary
    ai_results = []
    for index, row in df_test.iterrows():
        print(f"Processing article {index + 1}...")
        result = extract_structured_data(row['summary'])
        ai_results.append(result)
        time.sleep(2) # Pause to respect API rate limits
        
    # 6. Convert the list of JSON results into columns and merge them
    ai_df = pd.DataFrame(ai_results)
    enriched_df = pd.concat([df_test.reset_index(drop=True), ai_df], axis=1)
    
    print("\nTransformation Complete! Here is the structured data:")
    print(enriched_df[['title', 'category', 'sentiment']].head())
    
    # 7. Save the final structured output
    enriched_df.to_csv("enriched_data.csv", index=False)
    print("\nSaved to enriched_data.csv")
