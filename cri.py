import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, UTC
from time import sleep

load_dotenv()  # Load environment variables from .env

class ICMFetcher:
    def __init__(self, uri, bearer_token):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.all_incidents = []

    def fetch_all_incidents(self, page_size=100):
        skip = 0
        while True:
            paged_uri = f"{self.uri}&$skip={skip}"
            response = requests.get(paged_uri, headers=self.headers)
            data = response.json()
            incidents = data.get("value", [])
            if not incidents:
                break
            self.all_incidents.extend(incidents)
            skip += page_size
        print(f"Total incidents fetched: {len(self.all_incidents)}")
        return self.all_incidents


class ICMDescriber:
    def __init__(self, uri, bearer_token, incidents):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }   
        self.incidents = incidents
        

    def describe_incidents(self):
        for incident in self.incidents:
            incident_id = incident.get("Id")
            if not incident_id:
                continue
            #print(f"\nDescribing incident with ID: {incident_id}")
            describe_uri = f"{self.uri}({incident_id})/GetIncidentDetails?$expand=CustomFields"
            response = requests.get(describe_uri, headers=self.headers)
        
            if response.status_code == 200:
                incident_details = response.json()
                #print(f"Incident ID: {incident_details}")
                #print(f"Custom Fields: {incident_details.get('CustomFields', [])}")
                for field in incident_details.get("CustomFields", []):
                    if "Name" in field and field["Name"] == "JiraIssueId":
                        print(f"{incident_id} - Jira ID: {field.get('StringValue')}")
                    else:
                        continue
                        
                
    



if __name__ == "__main__":
    uri = os.getenv("ICM_CRI_LIST")
    mitigater_uri = os.getenv("ICM_URI")
    bearer_token = os.getenv("ICM_BEARER_TOKEN")

    fetcher = ICMFetcher(uri, bearer_token)
    incidents = fetcher.fetch_all_incidents()


    describer = ICMDescriber(mitigater_uri, bearer_token, incidents)
    describer.describe_incidents()