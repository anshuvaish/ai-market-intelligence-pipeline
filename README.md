# 🚀 Automated AI Market Intelligence Pipeline

## 📊 Overview
An end-to-end, zero-touch ETL data pipeline that automatically aggregates daily news, utilizes Large Language Models (LLMs) for unstructured data extraction and sentiment analysis, and loads deduplicated records into a live stakeholder dashboard. 

## 🏗️ Architecture & Workflow
1. **Extract:** A Python script fetches daily unstructured text data via live RSS feeds.
2. **Transform:** Google's Gemini 2.5 Flash model processes the raw text via API, extracting key entities, categorizing topics, and assigning sentiment scores using strict JSON schema prompting.
3. **Load:** The data is transformed via Pandas, deduplicated against historical records using a primary key (URL), and pushed to a live Google Sheet via the Google Drive/Sheets API.
4. **Automate:** GitHub Actions CI/CD orchestrates the entire pipeline on a daily CRON schedule, ensuring the dashboard is continuously updated without manual intervention.

## 🛠️ Tech Stack
* **Language:** Python 3.10
* **Data Processing:** Pandas, Feedparser
* **AI & APIs:** Google GenAI SDK (Gemini), Gspread, OAuth2
* **Cloud & Automation:** GitHub Actions (CI/CD), Google Cloud Console (IAM & Service Accounts)
* **Presentation:** Google Sheets (Advanced QUERY and Array functions)

## 📈 Live Presentation Layer
**[Link to Live Automated Dashboard]**( [https://docs.google.com/spreadsheets/d/1SDo-iyNjnRvKWfubVodxjFXjlbSCRlHuFfP3mFq-l50/edit?usp=sharing] )

*Note: The dashboard updates automatically every day at 7:30 AM IST.*
