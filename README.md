# Finploy Interview Reminder Automation
Automated WhatsApp interview reminders for Finploy using GitHub Actions, Google Sheets API, and the WatiFly WhatsApp API.

This repository contains a fully cloud-automated workflow that:
- Fetches interview candidates from a Google Sheet
- Filters candidates whose interview is TOMORROW
- Sends WhatsApp reminder messages to ALL candidates
- Runs automatically every day at 5:00 PM IST
- Requires zero manual effort once deployed

---

## 📌 Project Structure

finploy_interview_reminder/
│
├── single_script.py # Main automation script (fetch + blast)
├── requirements.txt # Python dependencies
└── .github/
└── workflows/
└── interview_blast.yml # GitHub Actions workflow


---

## ⚙️ How the Automation Works

### 1️⃣ GitHub Actions triggers automatically at **5:00 PM IST**
The workflow uses a cron schedule:



30 11 * * * # 11:30 UTC = 5:00 PM IST


You can also trigger it manually from GitHub → Actions → Run Workflow.

---

### 2️⃣ The workflow loads secure credentials
A single encrypted secret is required:



FINPLOY_ENV


This JSON contains:
- Google Service Account credentials  
- WatiFly API credentials  

The workflow writes this JSON into:



finploy_env.json


inside the runner.

---

### 3️⃣ `single_script.py` executes the entire logic
The script performs:

#### ✔ Authenticate with Google Sheets  
Using the service account inside FINPLOY_ENV.

#### ✔ Read sheet "Tracker -Candidates" → tab "LINEUP"

#### ✔ Identify tomorrow’s date  
Example:



If today = 09-12-2025 → Target = 10-12-2025


#### ✔ Filter candidates whose "Interview Date" matches tomorrow

#### ✔ Send WhatsApp reminder messages to ALL candidates  
Using WatiFly template variables:

- Name  
- Company applied  
- Role  
- Location  
- Recruiter  

#### ✔ Does NOT modify Google Sheet  
No updating of Interview_msg_sent or any column.

---

## 🔐 Required GitHub Secret: FINPLOY_ENV

Go to:



Settings → Secrets → Actions → New repository secret


Name:



FINPLOY_ENV


Value:



{
"google_service_account": { ... },
"watifly": { ... }
}


This file must include:
- Google service account keys  
- WatiFly vendor UID  
- API token  
- Phone number ID  
- Template name  
- Template language  

---

## 🚀 Deployment Instructions

### Step 1 — Create repository  
Empty repo → upload files → commit.

### Step 2 — Add FINPLOY_ENV to GitHub Secrets  
Paste the full combined JSON as the secret value.

### Step 3 — Push workflow and code  
GitHub Actions will automatically detect everything.

### Step 4 — Test manually (optional)
Go to:



GitHub → Actions → Daily Interview Blast → Run Workflow


### Step 5 — Done  
Your automation runs daily without any manual work.

---

## 🛠️ File Details

### **single_script.py**
The core Python script that:
- Loads environment JSON  
- Connects to Google Sheets  
- Reads candidates  
- Filters by tomorrow  
- Sends WhatsApp messages  

### **interview_blast.yml**
Defines automated GitHub Action:
- Runs every day at 5 PM IST  
- Installs dependencies  
- Creates finploy_env.json  
- Runs single_script.py  

### **requirements.txt**
Required Python modules:


pandas
gspread
google-auth
google-auth-oauthlib
google-auth-httplib2
requests
openpyxl


---

## 🧪 Testing

To test the setup without waiting for cron:



GitHub → Actions → Daily Interview Blast → Run workflow


Watch logs live in GitHub Actions.

---

## 📞 Support / Contact

For internal Finploy operations or DevOps support, contact:
- Harsh (Automation)
- Finploy Tech Team

---

## ✔️ Status: Production Ready

This workflow is optimized for:
- Zero maintenance  
- Full cloud execution  
- Secure credential management  
- Automatic WhatsApp reminders  

Once configured, it will run daily without fail.
