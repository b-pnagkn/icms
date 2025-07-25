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

class ICMAnalyzer:
    def __init__(self, incidents):
        self.incidents = incidents

    def list_titles_before(self):
        cutoff = datetime(2025, 5, 1, tzinfo=UTC)
        old_incidents = []
        for incident in self.incidents:
            created_str = incident.get("CreatedDate")
            owner = incident.get("ContactAlias")
            id = int(incident.get("Id"))
            exception_icm_ids = [
    624516593,
    623701919
]
            if created_str:
                try:
                    try:
                        created_date = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
                    except ValueError:
                        created_date = datetime.strptime(created_str[:10], "%Y-%m-%d").replace(tzinfo=UTC)
                    if created_date < cutoff and not owner and id not in exception_icm_ids:
                        old_incidents.append(incident)
                except Exception as e:
                    print(f"Error parsing date '{created_str}': {e}")
                    continue
        # Print grouped results
        for inc in old_incidents:
            print(f"  Id: {inc.get('Id')}, CreatedDate: {inc.get('CreatedDate')}")
        print(f"Total grouped titles without owner before May 2025: {len(old_incidents)}")
        return old_incidents

class ICMMitigater:
    def __init__(self, uri, bearer_token, incidents):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.incidents = incidents
    
    def mitigate_incidents(self):
        for incident in self.incidents:
            print(incident)
            incident_id = incident.get("Id")
            if not incident_id:
                print("Incident ID not found, skipping resolution.")
                continue
            print(f"Mitigating incident with ID: {incident_id}")
            payload = {
                "MitigateParameters": {
                    "IsCustomerImpacting": "False",
                    "IsNoise": "True",
                    "Mitigation": "Cleaning up IcMs which are created before May 1st, 2025 & have no owner",
                    "HowFixed": "Mitigated as part of cleanup process",
                    "MitigateContactAlias": "b-pnagkn"
                }
            }

            mitigate_uri = f"{self.uri}({incident_id})/MitigateIncident"
            print("mitigate:", mitigate_uri)
            response = requests.post(mitigate_uri, headers=self.headers, json=payload)
            if response.status_code == 200:
                print(f"Incident {incident_id} mitigated successfully.")
            else:
                print(f"Failed to mitigate incident: {response.status_code} - {response.text}")
            sleep(10)

class ICMResolver:
    def __init__(self, uri, bearer_token, incidents):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.incidents = incidents


    def resolve_incidents(self):
        #for incident in self.incidents:
        #    incident_id = incident.get("Id")
        #    if not incident_id:
        #        print("Incident ID not found, skipping resolution.")
        #        continue
        
        incident_id = "560602092" #Example Incident ID
        resolve_uri = f"{self.uri}({incident_id})/ResolveIncident"

        payload = {
            "ResolveParameters" : {
                "IsCustomerImpacting" : "False", 
                "IsNoise" : "True", 
                "Description" : { 
                    "Text" : "Resolving from the script", 
                    "RenderType" : "Plaintext"
                }, 
                "ResolveContactAlias" : "b-pnagkn" 
                }   
        }
        
        print(f"Resolving URI: {resolve_uri}")
        
        response = requests.post(resolve_uri, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            print(f"Incident {incident_id} resolved successfully.")
        else:
            print(f"Failed to resolve incident {incident_id}: {response.status_code} - {response.text}")


class ICMDescriber:
    def __init__(self, uri, bearer_token, incident_id):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }   
        self.incident_id = incident_id
        

    def describe_incidents(self):
        print(f"\nDescribing incident with ID: {self.incident_id}")
        describe_uri = f"{self.uri}({self.incident_id})/GetIncidentDetails"
        response = requests.get(describe_uri, headers=self.headers)
        
        if response.status_code == 200:
            incident_details = response.json()
            print(f"Incident ID: {incident_details.get('Id')}")
            print(f"Title: {incident_details.get('Title')}")
            print(f"Created Date: {incident_details.get('CreatedDate')}")
            print(f"State: {incident_details.get('State')}")
            print(f"Severity: {incident_details.get('Severity')}")
            print(f"Owning Team: {incident_details.get('OwningTeamName')}")
        else:
            print(f"Failed to describe incident: {response.status_code} - {response.text}") 

if __name__ == "__main__":
    uri = os.getenv("ICM_LIST_URI")
    mitigater_uri = os.getenv("ICM_URI")
    bearer_token = os.getenv("ICM_BEARER_TOKEN")

    # fetcher = ICMFetcher(uri, bearer_token)
    # incidents = fetcher.fetch_all_incidents()

    # analyzer = ICMAnalyzer(incidents)
    # old_incidents = analyzer.list_titles_before()

    # describer = ICMDescriber(mitigater_uri, bearer_token, "380355203")
    # describer.describe_incidents()

    # mitigater = ICMMitigater(mitigater_uri, bearer_token, old_incidents)
    # mitigater.mitigate_incidents()

    # resolver = ICMResolver(mitigater_uri, bearer_token, [])
    # resolver.resolve_incidents()
