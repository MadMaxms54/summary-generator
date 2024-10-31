import pandas as pd

# Use one of the approaches mentioned above
excel_file_path = r"C:\Users\essak\Downloads\muthu.xlsx"

# Read the Excel file
df = pd.read_excel(excel_file_path)

# Assuming names are in a column named 'Name'
names = df['Name'].tolist()  # Convert the column to a list

# Print the collected names
print(names)
