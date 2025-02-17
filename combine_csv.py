import pandas as pd
import os

# List of CSV files to combine
csv_files = [
    'lotto_prize_1th.csv',
    'lotto_prize_2digit.csv',
    'lotto_nearby_1th.csv',
    'lotto_prize_3digit_fixed.csv',
    'lotto_prize_2nd.csv',
    'lotto_prize_3rd.csv',
    'lotto_prize_4th.csv',
    'lotto_prize_5th.csv',
]

# Initialize an empty DataFrame
combined_df = pd.DataFrame()

# Iterate through the list of CSV files and concatenate them
for file in csv_files:
    if os.path.exists(file):
        df = pd.read_csv(file)
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on='date', how='outer')

# Save the combined DataFrame to a new CSV file
combined_df.to_csv('lotto_prize_combined.csv', index=False)
