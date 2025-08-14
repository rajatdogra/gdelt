import pandas as pd

print("Starting data processing...")
# === Step 1: Load CSV ===
input_file = 'bquxjob_3fa353a7_198845fe64c.csv'       # Replace with your actual file name
output_file = 'bquxjob_3fa353a7_198845fe64c_dedup.csv'   # Output file name

try:
    df = pd.read_csv(input_file)

    # === Step 2: Drop Duplicates Based on SourceUrl ===
    df_cleaned = df.drop_duplicates(subset='SourceUrl', keep='first')

    # === Step 3: Save Cleaned CSV ===
    df_cleaned.to_csv(output_file, index=False)

    print(f"✅ Duplicates removed. Cleaned data saved to '{output_file}'.")
    print(f"Original rows: {len(df)}, After cleaning: {len(df_cleaned)}")

except FileNotFoundError:
    print(f"❌ File '{input_file}' not found. Please check the file name and path.")
except Exception as e:
    print(f"❌ An error occurred: {e}")
