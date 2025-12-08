# Finploy Interview Reminder Automation

Automated WhatsApp interview reminders for Finploy using GitHub Actions, Google Sheets API, and the WatiFly WhatsApp API.

This repository contains a fully cloud-automated workflow that:
- Fetches interview candidates from a Google Sheet
- Filters candidates scheduled for TOMORROW
- Sends WhatsApp reminder messages to ALL of them
- Runs automatically every day at 5:00 PM IST
- Requires zero manual effort once deployed
```bash
📌 Project Structure

finploy_interview_reminder/
│
├── single_script.py                 # Main automation script (fetch + blast)
├── requirements.txt                 # Python dependencies
└── .github/
    └── workflows/
        └── interview_blast.yml      # GitHub Actions workflow
⚙️ How It Works

1️⃣ GitHub Actions triggers daily at 5:00 PM IST  
   Cron used: 30 11 * * *   (11:30 UTC = 5 PM IST)

2️⃣ FINPLOY_ENV secret is loaded  
   Contains:
   - Google service account JSON  
   - WatiFly API credentials

3️⃣ Script generates tomorrow’s date  
   Example:  
   If today = 09-12-2025 → target = 10-12-2025

4️⃣ Script fetches "Tracker -Candidates" → "LINEUP"

5️⃣ Filters rows where:
   Interview Date == target tomorrow

6️⃣ Sends WhatsApp reminders using fields:
   - Name  
   - Company applied  
   - Role  
   - Location  
   - Recruiter

7️⃣ Sheet is NOT modified (as required)
🔐 Required GitHub Secret: FINPLOY_ENV

Go to:
Repo → Settings → Secrets → Actions → New repository secret

Name:
FINPLOY_ENV

Value:
{
  "google_service_account": { ... },
  "watifly": { ... }
}

This JSON must contain BOTH:
- Google Service Account credentials
- WatiFly API credentials

🚀 Deployment Steps

1️⃣ Create a new GitHub repository  
2️⃣ Upload these files:
    - single_script.py
    - requirements.txt
    - .github/workflows/interview_blast.yml
3️⃣ Add FINPLOY_ENV secret
4️⃣ Push commit
5️⃣ Automation begins immediately
'''
```
🛠 File: single_script.py

Performs:
- Load FINPLOY_ENV
- Authenticate Google Sheets
- Compute tomorrow's date
- Fetch interview candidates
- Send WhatsApp reminders via WatiFly
