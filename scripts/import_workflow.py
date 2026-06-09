import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

N8N_HOST = os.getenv("N8N_HOST")
API_KEY = os.getenv("N8N_API_KEY")
WORKFLOW_FILE = "NasetOFM_AI_Pipeline_v1.json"

with open(WORKFLOW_FILE, "r") as f:
    workflow_data = json.load(f)

# Ne pas envoyer les champs en lecture seule
workflow_data.pop("id", None)
workflow_data.pop("versionId", None)
workflow_data.pop("meta", None)

response = requests.post(
    f"{N8N_HOST}/rest/workflows",
    headers={"X-N8N-API-KEY": API_KEY, "Content-Type": "application/json"},
    json=workflow_data
)

if response.status_code in (200,201):
    print("Workflow importé avec succès")
    print(f"ID du workflow: {response.json()['id']}")
else:
    print(f"Erreur: {response.status_code}")
    print(response.text)