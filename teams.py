import pandas as pd
import io
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def create_icm_excel(title_groups, filename="icm_grouped.xlsx"):
    excel_data = []
    for title, incidents in title_groups.items():
        for inc in incidents:
            excel_data.append({
                "Title Group": title,
                "Id": inc.get('Id'),
                "Severity": inc.get('Severity'),
                "State": inc.get('State'),
                "CreatedDate": inc.get('CreatedDate'),
                "ContactAlias": inc.get('ContactAlias')
            })
    df = pd.DataFrame(excel_data)
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    with open(filename, "wb") as f:
        f.write(excel_buffer.read())
    return filename

def send_teams_message(webhook_url, message):
    response = requests.post(
        webhook_url,
        json={"text": message}
    )
    return response.status_code

def send_graph_message(access_token, user_id, message):
    # 1. Create a chat (if not already exists)
    chat_payload = {
        "chatType": "oneOnOne",
        "members": [
            {
                "@odata.type": "#microsoft.graph.aadUserConversationMember",
                "roles": ["owner"],
                "user@odata.bind": f"https://graph.microsoft.com/v1.0/users('{user_id}')"
            }
        ]
    }
    chat_response = requests.post(
        "https://graph.microsoft.com/v1.0/chats",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json=chat_payload
    )
    chat_id = chat_response.json()["id"]

    # 2. Send a message
    message_payload = {
        "body": {
            "contentType": "text",
            "content": message
        }
    }
    msg_response = requests.post(
        f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages",
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"},
        json=message_payload
    )
    return msg_response.status_code

def send_grouped_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        with open(attachment_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=attachment_path)
        part['Content-Disposition'] = f'attachment; filename="{attachment_path}"'
        msg.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

# Example usage:
# filename = create_icm_excel(title_groups)
# status = send_teams_message("YOUR_TEAMS_WEBHOOK_URL", f"ICM Grouped Report generated: {filename}. Please download from your secure location.")
# print(f"Teams message sent, status code: {status}")
# graph_status = send_graph_message("YOUR_ACCESS_TOKEN", "USER_OBJECT_ID", "ICM Grouped Report generated. Please download from your secure location.")
# print(f"Graph message sent, status code: {graph_status}")
# send_grouped_email(
#     smtp_server="smtp.office365.com",
#     smtp_port=587,
#     sender_email="your_email@domain.com",
#     sender_password="your_password",
#     recipient_email="recipient@domain.com",
#     subject="ICM Grouped Report",
#     body="Please find attached the latest ICM grouped report.",
#     attachment_path=filename
# )