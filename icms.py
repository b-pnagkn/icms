import requests
from datetime import datetime, timedelta
import difflib
import re
from teams import create_icm_excel, send_teams_message, send_grouped_email

# Define the API endpoint
uri = "https://prod.microsofticm.com/api2/user/incidentapi/incidents?$select=Id,Severity,State,Title,CreatedDate,OwningTenantName,OwningTeamName,ContactAlias,NotificationStatus,HitCount,ChildCount,OwningServiceId,ServiceCategoryId,OwningTeamId,AcknowledgeBy,ParentId,CustomerName,RootCause,Postmortem,IsCustomerImpacting,IsNoise,IsOutage,ExternalLinksCount,CustomFields,AlertSource,Bridges&$filter=((OwningServiceId%20eq%2023111)%20and%20(OwningTeamId%20eq%2042908)%20and%20Type%20eq%20%27LiveSite%27%20and%20State%20eq%20%27Active%27)%20%20and%20ParentId%20eq%20null&$expand=RootCause,CustomFields,AlertSource,Bridges&$skip=0"

# Define the bearer token
bearer_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IkVBMDlGNTkzNzM2QzA3QkQ5RTBCNjBENUNBQjIyMjAzRTE3RDQ0MjYiLCJ4NXQiOiI2Z24xazNOc0I3MmVDMkRWeXJJaUEtRjlSQ1kiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJzdmM6Ly9zc29AcHJvZC5taWNyb3NvZnRpY20uY29tLyIsImlhdCI6MTc1MzE1MzU5OCwibmJmIjoxNzUzMTUzNTk4LCJleHAiOjE3NTMxNjQzOTgsIl9jbGFpbV9uYW1lcyI6eyJncm91cHMiOiJzcmMxIn0sIl9jbGFpbV9zb3VyY2VzIjp7InNyYzEiOnsiZW5kcG9pbnQiOiJodHRwczovL2dyYXBoLndpbmRvd3MubmV0LzcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0Ny91c2Vycy80NWZjMTJlYy1hZjAwLTQ3MjItYWQ2Yi1jOWYzNDAxNTc2NGIvZ2V0TWVtYmVyT2JqZWN0cyJ9fSwiYWNjdCI6MCwiYWlvIjoiQWFRQVcvOFpBQUFBR280aklPdlhNek55YVZaR0FzQjlPZ3l3Q2JndlNuK1BjWUVIMkc4a001QVBZZDVJTzhTOWlvZE9PbEhjZ0Z5QXpnSlFBa0tYczRZa1p6bDBEODBuNmlNeHRnTzNWRDBLdFJGN0pTMk5sd21aOVF4MHRFM1c3YTFzSU5GMFJObzlyaEFHcTF6dWtZNzhZS3FReDJNODdYZmdzYUx2T1ZVMFdpWkFMc0xFTmZxVXBQY29CQjlpQXRsdHBTMkJ5UnAvVWl4TFNVbXJEWENsaHhWMnptTG1LUT09IiwiY19oYXNoIjoiOGVHQl94ZTNRaWtKQ21LZ3ROSk1idyIsImVtYWlsIjoiYi1wbmFna25AbWljcm9zb2Z0LmNvbSIsImZhbWlseV9uYW1lIjoiTmFnIEsgTiIsImdpdmVuX25hbWUiOiJQcmF0aGliaGEiLCJpcGFkZHIiOiI0MC4xMTcuNjYuMTYiLCJuYW1lIjoiUHJhdGhpYmhhIE5hZyBLIE4gKE5FVEFQUCBJTkMpIiwibm9uY2UiOiI2Mzg4ODY5MTA3NzUzNjk0NTIuTWpObU1qa3pabUV0TmpRek15MDBPR1k0TFRsa1l6RXRabU0yTVROalkyRXdZelk1TWpka01URXhNV0V0TW1SbU1pMDBNRFZtTFRrMFkyUXRNVGd3WWpJek1UUmpaVGhoIiwib2lkIjoiNDVmYzEyZWMtYWYwMC00NzIyLWFkNmItYzlmMzQwMTU3NjRiIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiYi1wbmFna25AbWljcm9zb2Z0LmNvbSIsInJoIjoiMS5BUm9BdjRqNWN2R0dyMEdScXkxODBCSGJSNllmUWd3cklGMURwcE9RbV81NkhNSWFBS29hQUEuIiwic2lkIjoiMDA2ZTBiZjktNjRmYS1mN2FkLTVlZjMtMmVmM2Q3ZTRjZDc3IiwibmFtZWlkIjoid1ZoT3hwRVhUMkkzbzRPSHVXcUJPMjdtQlV1NU9uUXFwRTlxTGZTWll3MCIsInRpZCI6IjcyZjk4OGJmLTg2ZjEtNDFhZi05MWFiLTJkN2NkMDExZGI0NyIsInVwbiI6ImItcG5hZ2tuQG1pY3Jvc29mdC5jb20iLCJ1dGkiOiJBRFk0SFdQOGkwU3pHNklKQlA5ZkFBIiwidmVyIjoiMi4wIiwidmVyaWZpZWRfcHJpbWFyeV9lbWFpbCI6ImItcG5hZ2tuQG1pY3Jvc29mdC5jb20iLCJ2ZXJpZmllZF9zZWNvbmRhcnlfZW1haWwiOlsiYi1wbmFna25AbWljcm9zb2Z0Lm9ubWljcm9zb2Z0LmNvbSIsImItcG5hZ2tuQHNlcnZpY2UubWljcm9zb2Z0LmNvbSJdLCJ3aWRzIjoiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5IiwiZ3JvdXAiOlsiUkVETU9ORFxcTkVUQVBQIEFaVVJFIFRFQU0iLCJSRURNT05EXFxBWlVSRS1BTEwtUFNWIiwiUkVETU9ORFxcVE0tQXp1cmVOZXRBcHAtUlctNmFiZCIsIlJFRE1PTkRcXEFaVVJFLUFMTC1TVEQiLCJSRURNT05EXFxBWlVSRSBORVRBUFAgRklMRVMgKERPTUFJTiBMT0NBTCkiXSwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0aWNtLmNvbS9Hcm91cE1lbWJlcnNoaXBGZXRjaGVkRnJvbU1zR3JhcGgiOlsidHJ1ZSIsInRydWUiLCJ0cnVlIiwidHJ1ZSIsInRydWUiLCJ0cnVlIiwidHJ1ZSJdLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL2FjY2Vzc2NvbnRyb2xzZXJ2aWNlLzIwMTAvMDcvY2xhaW1zL2lkZW50aXR5cHJvdmlkZXIiOiJzdmM6Ly9zc29AcHJvZC5taWNyb3NvZnRpY20uY29tLyIsImh0dHA6Ly9zdHMubXNmdC5uZXQvdXNlci91cG4iOiJiLXBuYWdrbkBtaWNyb3NvZnQuY29tIiwiYXVkIjoiaHR0cHM6Ly9wcm9kLm1pY3Jvc29mdGljbS5jb20ifQ.fxVSGsSemKlL36EpN2u8h7aMePEWQMqYSevqQhdFkYmHZWnNIY_VaGDyyfiF0wfhQYm8yRm8ZLkngo0c0gqIVf32uLCHYA5y5LIyVmcdMG-VAGKatoP4zAzQs5CvK0YewROseybc6kXLAwUu7QLvZ2n7aMw_xV8prgiDRRSbmVPX-N_LiofwVPG2zvxpO4DUPzQ5-h0fNowVR-A0y5wfiMeXEp5uZCE_qGhW863BH3ZApCCG4p4UKXYk6n-Gm0p6wP87989c55Hd2iRjAocQg_SwyqL9PpvgiODBenRSD9XqKt1Mwh2pg54ja0mzYCrOPxxmYytcOcvtcDerCFxhQA"

# Define the headers
headers = {
    "Authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

# Make the GET request
response = requests.get(uri, headers=headers)

# Group incidents by title
data = response.json()
title_groups = {}
for incident in data.get("value", []):
    title = incident.get("Title", "Unknown")
    if title not in title_groups:
        title_groups[title] = []
    title_groups[title].append(incident)

# Print grouped titles and their incidents
for title, incidents in title_groups.items():
    print(f"Title: {title} (Count: {len(incidents)})")
    for inc in incidents:
        print(f"  Id: {inc.get('Id')}, Severity: {inc.get('Severity')}, State: {inc.get('State')}")

def normalize_title(title):
    # Remove region info like [East US], (West Europe), etc.
    return re.sub(r"[\[\(].*?[\]\)]", "", title).strip().lower()

def find_similar_title(title, groups, threshold=0.8):
    norm_title = normalize_title(title)
    for existing_title in groups:
        if difflib.SequenceMatcher(None, norm_title, normalize_title(existing_title)).ratio() >= threshold:
            return existing_title

# Group incidents by similar titles (excluding region info)
title_groups = {}
for incident in data.get("value", []):
    title = incident.get("Title", "Unknown")
    similar_title = find_similar_title(title, title_groups)
    if similar_title:
        title_groups[similar_title].append(incident)
    else:
        title_groups[title] = [incident]

# Print grouped similar titles and their incidents
for title, incidents in title_groups.items():
    print(f"Title Group: {title} (Count: {len(incidents)})")
    for inc in incidents:
        print(f"  Id: {inc.get('Id')}, Severity: {inc.get('Severity')}, State: {inc.get('State')}")
    print()

# List all ICMs created 60 days before today
days_before = 60
cutoff_date = datetime.utcnow() - timedelta(days=days_before)

print(f"ICMs created exactly {days_before} days before today ({cutoff_date.date()}):")
for incident in data.get("value", []):
    created_str = incident.get("CreatedDate")
    if created_str:
        try:
            created_date = datetime.strptime(created_str[:10], "%Y-%m-%d")
            if created_date.date() == cutoff_date.date():
                print(f"Id: {incident.get('Id')}, Title: {incident.get('Title')}, CreatedDate: {created_str}")
        except Exception:
            continue

# Create Excel file from grouped incidents
excel_filename = create_icm_excel(title_groups)

# Send Teams message with info about the report
#teams_webhook_url = "YOUR_TEAMS_WEBHOOK_URL"  # Replace with your actual webhook URL
##status = send_teams_message(
  #  teams_webhook_url,
  #  f"ICM Grouped Report generated: {excel_filename}. Please download from your secure location."
#)
#print(f"Teams message sent, status code: {status}")

# Send grouped report via email
#send_grouped_email(
 #   smtp_server="smtp.office365.com",
  #  smtp_port=587,
   # sender_email="pn96195@netapp.com",         # Replace with your email
    #sender_password="jusbej-0Simdo-tuwqug",              # Replace with your password
 #   recipient_email="pn96195@netapp.com",       # Replace with recipient's email
  #  subject="ICM Grouped Report",
   # body="Please find attached the latest ICM grouped report.",
    #attachment_path=excel_filename
#)
#print("Email sent.")

import requests

def send_slack_message(webhook_url, message):
    response = requests.post(
        webhook_url,
        json={"text": message}
    )
    return response.status_code

# Example usage:
slack_webhook_url = "https://hooks.slack.com/services/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"  # Replace with your Slack webhook URL
status = send_slack_message(
    slack_webhook_url,
    f"ICM Grouped Report generated: {excel_filename}. Please check your email for the attached report."
)
print(f"Slack message sent, status code: {status}")

def send_slack_file(token, channel, file_path, message):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://slack.com/api/files.upload",
            headers={"Authorization": f"Bearer {token}"},
            data={
                "channels": channel,
                "initial_comment": message,
                "title": "ICM Grouped Report"
            },
            files={"file": f}
        )
    return response.status_code, response.json()

# Example usage:
slack_bot_token = "xoxb-9017150674517-9156082369943-ygeObAWfZN0nPC2ZKvnvUaEN"  # Replace with your Slack bot token
slack_channel = "C0958P8D6DU"                # Replace with your channel name or ID
status, resp = send_slack_file(
    slack_bot_token,
    slack_channel,
    excel_filename,
    "ICM Grouped Report generated. Please find the attached Excel file."
)

print(f"Slack file upload status: {status}, response: {resp}")
print(f"Slack file upload status: {status}, response: {resp}")
