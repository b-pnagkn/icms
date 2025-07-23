import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta, UTC

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
        grouped = {}
        for incident in self.incidents:
            created_str = incident.get("CreatedDate")
            owner = incident.get("ContactAlias")
            if created_str:
                try:
                    try:
                        created_date = datetime.strptime(created_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)
                    except ValueError:
                        created_date = datetime.strptime(created_str[:10], "%Y-%m-%d").replace(tzinfo=UTC)
                    if created_date < cutoff and not owner:
                        title = incident.get('Title', 'Unknown')
                        if title not in grouped:
                            grouped[title] = []
                        grouped[title].append(incident)
                except Exception as e:
                    print(f"Error parsing date '{created_str}': {e}")
                    continue
        # Print grouped results
        for title, incidents in grouped.items():
            print(f"Title: {title} (Count: {len(incidents)})")
            for inc in incidents:
                print(f"  Id: {inc.get('Id')}, CreatedDate: {inc.get('CreatedDate')}")
        print(f"Total grouped titles without owner before May 2025: {len(grouped)}")
        return grouped

class ICMMitigater:
    def __init__(self, uri, bearer_token, incidents):
        self.uri = uri
        self.headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }
        self.incidents = incidents
    
    def mitigate_incidents(self):
 #      for incident in self.incidents:
 #          incident_id = incident.get("Id")
 #          if not incident_id:
 #              print("Incident ID not found, skipping resolution.")
 #              continue
        incident_id = "612219907" #Example Incident ID
        res = requests.get("https://prod.microsofticm.com/api2/user/incidentapi/incidents(658065143)/GetIncidentDetails", headers= self.headers)
        
        payload = {
            "MitigateParameters": {
                "IsCustomerImpacting": "False",
                "IsNoise": "True",
                "Mitigation": "Cleaning up IcMs which are created before April 1st, 2025 & have no owner",
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
        

if __name__ == "__main__":
    uri = os.getenv("ICM_LIST_URI")
    mitigater_uri = os.getenv("ICM_URI")
    bearer_token = os.getenv("ICM_BEARER_TOKEN")

    fetcher = ICMFetcher(uri, bearer_token)
    incidents = fetcher.fetch_all_incidents()

    analyzer = ICMAnalyzer(incidents)
    old_incidents = analyzer.list_titles_before()

#   for incident in old_incidents:
#       print("Incident ID & Titile:", incident.get("Id"), incident.get("Title"), "CreatedDate:", incident.get("CreatedDate"))


    mitigater = ICMMitigater(mitigater_uri, bearer_token, [])
    mitigater.mitigate_incidents()

    # resolver = ICMResolver(mitigater_uri, bearer_token, [])
    # resolver.resolve_incidents()
