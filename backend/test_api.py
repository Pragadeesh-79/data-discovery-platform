import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    print(f"Testing GET {BASE_URL}/ ...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}\n")

def test_status():
    print(f"Testing GET {BASE_URL}/status ...")
    response = requests.get(f"{BASE_URL}/status")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}\n")

def test_scan_results():
    print(f"Testing POST {BASE_URL}/scan-results ...")
    mock_pii_record = {
        "type": "Email",
        "value": "test@example.com",
        "location": "test_folder/test.txt",
        "source": "local_folder",
        "owner": "IT",
        "sensitivity": "Low",
        "risk_score": 10
    }
    response = requests.post(f"{BASE_URL}/scan-results", json=mock_pii_record)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.json()}\n")

if __name__ == "__main__":
    # Wait a moment for server to start if running alongside
    time.sleep(2)
    test_root()
    test_status()
    test_scan_results()
