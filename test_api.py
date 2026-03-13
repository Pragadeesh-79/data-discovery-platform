import requests
import json

BASE_URL = "http://localhost:8000"

records = [
    {"type": "Email", "value": "test@example.com", "location": "hr/employees.csv", "source": "local_folder", "owner": "HR", "sensitivity": "Low", "risk_score": 2},
    {"type": "PAN", "value": "ABCDE1234F", "location": "finance/data.xlsx", "source": "local_folder", "owner": "Finance", "sensitivity": "High", "risk_score": 8},
    {"type": "Phone", "value": "9876543210", "location": "marketing/leads.csv", "source": "local_folder", "owner": "Marketing", "sensitivity": "Medium", "risk_score": 5},
    {"type": "Aadhaar", "value": "123456789012", "location": "hr/kyc_docs.pdf", "source": "local_folder", "owner": "HR", "sensitivity": "High", "risk_score": 9},
    {"type": "Name", "value": "Rahul Sharma", "location": "public/contacts.txt", "source": "local_folder", "owner": "Public", "sensitivity": "Low", "risk_score": 1}
]

print("--- STEP 1: Insert Test Data ---")
for r in records:
    res = requests.post(f"{BASE_URL}/scan-results", json=r)
    print(res.status_code, res.json())

print("\n--- STEP 2: GET /inventory ---")
res = requests.get(f"{BASE_URL}/inventory")
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("\n--- STEP 3: GET /risk-summary ---")
res = requests.get(f"{BASE_URL}/risk-summary")
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("\n--- STEP 4: GET /pii-types ---")
res = requests.get(f"{BASE_URL}/pii-types")
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("\n--- STEP 5: GET /dpdpa-report ---")
res = requests.get(f"{BASE_URL}/dpdpa-report")
print(res.status_code)
print(json.dumps(res.json(), indent=2))

print("\n--- STEP 6: GET /dashboard-stats ---")
res = requests.get(f"{BASE_URL}/dashboard-stats")
print(res.status_code)
print(json.dumps(res.json(), indent=2))

