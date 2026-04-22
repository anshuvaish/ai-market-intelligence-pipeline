import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def push_to_google_sheets(csv_file, spreadsheet_name, worksheet_name="Sheet1"):
    print("Connecting to Google Sheets...")
    
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    
    try:
        sheet = client.open(spreadsheet_name).worksheet(worksheet_name)
        
        # 1. Read the NEW daily data from your Python script
        df_new = pd.read_csv(csv_file)
        df_new = df_new.fillna("")
        
        # 2. Fetch the EXISTING historical data currently in the Google Sheet
        print("Fetching historical data from the sheet...")
        existing_records = sheet.get_all_records()
        df_existing = pd.DataFrame(existing_records)
        
        # 3. Combine both datasets
        if not df_existing.empty:
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new
            
        # 4. Deduplicate using the 'link' as the Primary Key
        # If it sees the same URL twice, it drops the duplicate automatically
        initial_count = len(df_combined)
        df_combined = df_combined.drop_duplicates(subset=['link'], keep='first')
        duplicates_removed = initial_count - len(df_combined)
        
        print(f"Removed {duplicates_removed} duplicate articles.")
        
        # 5. Push the master deduplicated database back to the sheet
        sheet.clear()
        data_to_upload = [df_combined.columns.values.tolist()] + df_combined.values.tolist()
        
        print(f"Uploading {len(df_combined)} total unique records to the Dashboard...")
        sheet.update(range_name='A1', values=data_to_upload)
        
        print("Success! Master Data loaded into Google Sheets.")
        
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Could not find a spreadsheet named '{spreadsheet_name}'.")

if __name__ == "__main__":
    target_spreadsheet = "AI_News_Enrichment_Pipeline" 
    push_to_google_sheets("daily_enriched_data.csv", target_spreadsheet, "Raw Data")