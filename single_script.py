import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime, timedelta
import requests
import json
import traceback

# ====================================================
# LOAD ENV FILE (Google + Watifly)
# ====================================================
with open("finploy_env.json", "r") as f:
    ENV = json.load(f)

GOOGLE = ENV["google_service_account"]
WATI = ENV["watifly"]

# ====================================================
# GOOGLE AUTH
# ====================================================
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(GOOGLE, scopes=scope)
client = gspread.authorize(creds)

# ====================================================
# LOGGING FUNCTION
# ====================================================
def write_run_log(status, reason):
    """
    Writes a log entry to Script_Run_Log → Harsh_Python_Programs
    """

    try:
        sheet = client.open("Script_Run_Log").worksheet("Harsh_Python_Programs")

        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")

        row = [
            date_str,               # Date
            status,                 # Status (1 or 0)
            "Daily Interview Blast",# Name_python_program
            time_str,               # Time
            reason                  # Reason
        ]

        sheet.append_row(row)
        print("Run log updated successfully.")

    except Exception as e:
        print("Failed to write log:", e)


# ====================================================
# MAIN SCRIPT WRAPPED IN TRY/EXCEPT
# ====================================================
try:
    # ====================================================
    # WATIFLY CONFIG
    # ====================================================
    VENDOR_UID = WATI["vendor_uid"]
    TOKEN = WATI["token"]
    FROM_PHONE_NUMBER_ID = WATI["from_phone_number_id"]
    TEMPLATE_NAME = WATI["template_name"]
    TEMPLATE_LANGUAGE = WATI["template_language"]

    API_SEND = f"https://watifly.in/api/{VENDOR_UID}/contact/send-template-message?token={TOKEN}"
    headers_api = {"Content-Type": "application/json"}

    # ====================================================
    # GOOGLE SHEET CONFIG
    # ====================================================
    GOOGLE_SHEET_NAME = "Tracker -Candidates"
    TAB_NAME = "LINEUP"

    # ====================================================
    # FETCH SHEET DATA
    # ====================================================
    sheet = client.open(GOOGLE_SHEET_NAME).worksheet(TAB_NAME)
    df = pd.DataFrame(sheet.get_all_records()).fillna("")

    # ====================================================
    # TARGET DATE = TOMORROW
    # ====================================================
    today = datetime.now()
    target_date = (today + timedelta(days=1)).strftime("%d-%m-%Y")

    print("Running script for:", target_date)

    # ====================================================
    # REQUIRED COLUMNS
    # ====================================================
    required_cols = [
        "Interview Date",
        "Name",
        "Contact",
        "Company applied",
        "Role",
        "Location",
        "Recruiter"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise Exception(f"Missing columns in sheet: {missing}")

    # ====================================================
    # FILTER CANDIDATES
    # ====================================================
    df_filtered = df[df["Interview Date"] == target_date]

    print("Total candidates found for tomorrow:", len(df_filtered))

    # ====================================================
    # SEND WHATSAPP MESSAGES
    # ====================================================
    def send_message(name, phone, company, role, location, recruiter):
        payload = {
            "from_phone_number_id": FROM_PHONE_NUMBER_ID,
            "phone_number": "91" + phone,
            "template_name": TEMPLATE_NAME,
            "template_language": TEMPLATE_LANGUAGE,
            "field_1": name,
            "field_2": company,
            "field_3": role,
            "field_4": location,
            "field_5": recruiter
        }

        try:
            resp = requests.post(API_SEND, json=payload, headers=headers_api, timeout=20)
            return resp.json()
        except Exception as e:
            return {"result": "failed", "message": str(e)}

    # ====================================================
    # BLAST LOOP
    # ====================================================
    for _, row in df_filtered.iterrows():

        name = str(row["Name"])
        phone = str(row["Contact"]).replace(" ", "").replace("+91", "").strip()
        company = row["Company applied"]
        role = row["Role"]
        location = row["Location"]
        recruiter = row["Recruiter"]

        print(f"Sending → {name} ({phone})")

        response = send_message(name, phone, company, role, location, recruiter)

        print("Response:", response)

    print("\nAll messages sent successfully.")

    # ====================================================
    # WRITE SUCCESS LOG
    # ====================================================
    write_run_log(1, "Coder is great")

except Exception as e:
    print("SCRIPT FAILED:", e)
    print(traceback.format_exc())

    # ====================================================
    # WRITE FAILURE LOG
    # ====================================================
    write_run_log(0, str(e))
