# icms

## Overview

This script fetches, analyzes, and optionally mitigates or resolves ICM incidents using the Microsoft ICM API. It supports grouping incidents, filtering by date/owner, and can be extended to send notifications or reports.

---

## Prerequisites

- **Python 3.8+** (recommended: 3.10+)
- **Microsoft ICM API access** (with a valid Bearer Token)
- **ICM API URI** (for listing and mitigating incidents)
- **ICM Bearer Token** (with required permissions)

---

## Required Python Packages

Install these packages before running the script:

```sh
pip install requests python-dotenv pandas openpyxl
```

- `requests` - For making HTTP API calls
- `python-dotenv` - For loading environment variables from `.env`
- `pandas` and `openpyxl` - For Excel report generation (if needed)

---

## Setup

1. **Clone or download this repository.**

2. **Create a `.env` file** in the project directory with the following content:

    ```
    ICM_LIST_URI=your_icm_list_uri_here
    ICM_URI=your_icm_base_uri_here
    ICM_BEARER_TOKEN=your_bearer_token_here
    ```

    - Replace the values with your actual ICM API URIs and Bearer Token.

3. **(Optional) Configure additional environment variables** if you extend the script for Teams, Slack, or Email integration.

---

## Usage

Run the script from the command line:

```sh
python icms.py
```

The script will:
- Fetch all incidents using the ICM API.
- Group and print incidents created before April 1st, 2025, without an owner.
- (Optional) Mitigate or resolve incidents if you enable those features.

---

## Features

- **Fetch all ICM incidents** (handles pagination)
- **Group incidents by title**
- **Filter by creation date and owner**
- **Mitigate or resolve incidents via API**
- **Environment-based configuration**
- **Extensible for Teams, Slack, and Email notifications**

---

## Optional Plugins/Integrations

If you want to send notifications or reports, you may need:

- **Microsoft Teams integration:**  
  - [requests](https://pypi.org/project/requests/) (already required)
  - Teams webhook URL or Microsoft Graph API setup

- **Slack integration:**  
  - Slack Bot Token (for file uploads)
  - [requests](https://pypi.org/project/requests/)

- **Email integration:**  
  - SMTP server credentials
  - [smtplib](https://docs.python.org/3/library/smtplib.html) (standard library)

---

## Troubleshooting

- **401/403 errors:** Check your Bearer Token and permissions.
- **404 errors:** Check your ICM URI and incident IDs.
- **JSON decode errors:** Print the response text to debug API issues.
- **Characters replaced while typing:** Press `Insert` to toggle overwrite mode in your editor.

---

## License

Internal use only. Do not distribute outside
