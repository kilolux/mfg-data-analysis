#!/usr/bin/python

'''
google_sheet_to_sqlite_demo.py

This python script pulls down a Google Sheet
and converts it into a sqlite database, using
a pandas dataframe as an intermediary.

Link To Google Sheet:
https://docs.google.com/spreadsheets/d/<some-sheet-key>

Please note that this script will not function unless
you set the following two variables to your personal credentials.
(1) credentials_filename
(2) google_sheet_key

The libraries used are:
pandas: A data analysis and manipulation tool for python. 
	    More info at: https://pandas.pydata.org/
sqlite3: A lightweight database utility
gspread: The API library for accessing Google Sheets
oauth2: Google's implementation of the OAuth2.0 authentication framework
google.auth: Google's authentication library
'''

# Libraries
import pandas as pd
import sqlite3
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Get json credentials file
credentials_filename = 'your-file-goes-here.json'
credentials = service_account.Credentials.from_service_account_file(
    credentials_filename)

# Define scope URLs
scoped_credentials = credentials.with_scopes(
        ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        )

# Create client
gc = gspread.Client(auth=scoped_credentials)
gc.session = AuthorizedSession(scoped_credentials)

# Open a Google Sheet File
google_sheet_key = 'your-sheet-key-goes-here'
sheet = gc.open_by_key(google_sheet_key)

verbose_mode = False
if verbose_mode: print("sheet.title:",sheet.title + "\n")

# Open a specific worksheet from the Sheet file
worksheet = sheet.worksheet("Data")

# Convert worksheet into a pandas dataframe.
df = pd.DataFrame(worksheet.get_all_records())

# Check the first rows of the dataframe to see if the pandas import worked.
if verbose_mode:
	print("Checking dataframe:")
	print(df.head())

# Cleanup column names to all lowercase with underscores instead of spaces.
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
if verbose_mode:
	print("New column names:")
	print(df.head())

# Create a sqlite database named after the Google Sheet.
database_name = sheet.title + ".db"
table_name = "mfgdata"

# Try to connect to the database, otherwise quit.
try:
	conn = sqlite3.connect(database_name)
	print("Opening database: " + database_name + "\n")

except:
	print("Failed to connect to database.")
	quit()

# Export the dataframe into a sqlite database.
df.to_sql(table_name, conn, if_exists='append', index=False)

# Close the connnection.
conn.close()
print("Script 'google_sheet_to_sqlite_demo.py' finished. \n")