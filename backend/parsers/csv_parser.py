import pandas as pd

def parse_csv(file_path: str) -> str:
    try:
        df = pd.read_csv(file_path)
        return df.to_string(index=False)
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return ""
