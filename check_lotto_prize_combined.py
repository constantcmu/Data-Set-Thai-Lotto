import pandas as pd

def convert_date(date_str):
    year, month,date  = date_str.split('-')
    year = str(int(year) + 543)
    return f"{date}-{month}-{year}"

def check_and_convert_csv(file_path):
    df = pd.read_csv(file_path)
    df['date'] = df['date'].apply(convert_date)
    df.to_csv(file_path, index=False)
    print(f"Updated dates in {file_path}")

if __name__ == "__main__":
    file_path = 'lotto_prize_combined.csv'
    check_and_convert_csv(file_path)
