import requests

# Test JSON from the requirements
mock_data = {
  "file_name": "employees.csv",
  "source": "hr",
  "entity_type": "Aadhaar",
  "value": "123412341234",
  "classification": "Highly Sensitive"
}

print("Inserting mock data 1...")
res = requests.post("http://localhost:8000/scan-results", json=mock_data)
print(res.status_code, res.json())

mock_data_2 = {
  "file_name": "salaries.xlsx",
  "source": "finance",
  "entity_type": "PAN",
  "value": "ABCDE1234F",
  "classification": "Highly Sensitive"
}

print("Inserting mock data 2...")
res2 = requests.post("http://localhost:8000/scan-results", json=mock_data_2)
print(res2.status_code, res2.json())

print("Testing heatmap endpoint...")
res3 = requests.get("http://localhost:8000/reports/heatmap")
print(res3.status_code, res3.json())
