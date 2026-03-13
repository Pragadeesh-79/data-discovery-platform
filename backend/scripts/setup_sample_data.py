import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.database.mongo_client import sample_data_sources

sample_data = [
    {
        "source_type": "csv",
        "file_name": "employees.csv",
        "data": "Name,Phone,PAN,Aadhaar,Email\nRahul Sharma,9876543210,ABCDE1234F,123412341234,rahul.sharma@email.com\nAnita Verma,9123456780,FGHIJ5678K,987654321234,anita.verma@email.com"
    },
    {
        "source_type": "pdf",
        "file_name": "customer_data.pdf",
        "data": "Customer Name: Rajesh Kumar\nPhone: 9012345678\nPAN: PQRSX4321L\nAadhaar: 567812341234"
    },
    {
        "source_type": "email",
        "file_name": "customer_email.eml",
        "data": "Subject: Customer Verification\n\nHello,\n\nCustomer Name: Meera Nair\nPhone: 9988776655\nPAN: LMNOP1234Q\nAadhaar: 789012341234\n\nRegards\nSupport Team"
    },
    {
        "source_type": "database",
        "file_name": "customer_accounts",
        "data": "{\"name\": \"Arjun Menon\", \"phone\": \"9876501234\", \"pan\": \"ABCDE6789P\", \"aadhaar\": \"456712341234\", \"email\": \"arjun.menon@email.com\"}"
    }
]

def load_data():
    try:
        sample_data_sources.delete_many({}) # clear existing
        sample_data_sources.insert_many(sample_data)
        print("Sample data loaded successfully into MongoDB.")
    except Exception as e:
        print(f"Error loading sample data: {e}")

if __name__ == "__main__":
    load_data()
