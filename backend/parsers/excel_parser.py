import pandas as pd

def parse_excel(file_path: str) -> str:
    try:
        df = pd.read_excel(file_path)
        return df.to_string(index=False)
    except Exception as e:
        print(f"Error parsing Excel: {e}")
        return ""
