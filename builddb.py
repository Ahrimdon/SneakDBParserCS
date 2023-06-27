from bs4 import BeautifulSoup
import csv
import sqlite3
import requests
import os
import time

# Check if the 'temp' directory exists. If not, create it. We want this created before everything else.
if not os.path.exists('temp'):
    os.makedirs('temp')

def check_or_create_directories():
    # Check if the 'export' directory exists. If not, create it.
    if not os.path.exists('export'):
        os.makedirs('export')

    # Check if the 'sqlite_web_viewer/database' directory exists. If not, create it.
    if not os.path.exists('sqlite_web_viewer/database'):
        os.makedirs('sqlite_web_viewer/database')

# Check if MapDB.html exists
if os.path.isfile('temp/MapDB.html'):
    # Open the HTML file and parse it with BeautifulSoup
    with open("temp/MapDB.html", 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

        # Prompt the user for the webpage URL
        url = "https://snksrv.com/surfstats/?view=maps"

        # Fetch the webpage
        response = requests.get(url)

        # Save the webpage as MapDB.html
        with open('temp/MapDB.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Call the check_or_create_directories function
        check_or_create_directories()

        # Parse it with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

# Find the tables in the HTML
table = soup.find('table', class_="table table-striped table-hover sortable")

# Define the headers for the CSV files
headers_map_records = ["MapName", "MapTier", "WRTime", "WRHolder"]

# Create a SQLite connection and overwrite tables if they exist
conn = sqlite3.connect('MapDB.db')
c = conn.cursor()

# Delete the table if they already exist in the SQLite database
c.execute('''DROP TABLE IF EXISTS MapRecords;''')

# Create tables in the SQLite database
c.execute('''CREATE TABLE MapRecords
                (MapName text, MapTier text, WRTime text, WRHolder text,
                Completions text, AverageTime text, Bonuses text)''') 

csv_writers = {}

# Define the CSV file and SQLite table to write to based on the table index
csv_file = 'MapDB.csv'
headers = headers_map_records + ["Completions", "AverageTime", "Bonuses"]
table_name = 'MapRecords'

# Write to the CSV files
csv_writers[table_name] = csv.writer(open(os.path.join('export', csv_file), 'w', newline='', encoding='utf-8'))
csv_writers[table_name].writerow(headers)

# Write to the SQLite database
for row in table.findAll('tr'):
    columns = row.findAll('td')
    values = [col.text.strip() for col in columns]
    if values:
        # Write to the CSV file
        csv_writers[table_name].writerow(values)

        # Write to the SQLite database
        c.execute(f'INSERT INTO {table_name} (MapName, MapTier, WRTime, WRHolder) VALUES (?, ?, ?, ?)', values)

conn.commit()  # Commit after all inserts

# Create a new cursor for fetching data
c2 = conn.cursor()

# Fetch additional data
for row in c2.execute('SELECT MapName FROM MapRecords WHERE Completions IS NULL'):
    map_name = row[0]
    url = f"https://snksrv.com/surfstats/?view=map&name={map_name}"
    # Ask the user if they want to download all map info
    download = input(f"Do you want to download additional map information? (y/N) ")
    if download.lower() != 'y':
        continue

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    subheader = soup.find('div', class_='subheader')
    b_tags = subheader.find_all('b')

    completions = b_tags[0].text.split(': ')[1]
    average_time = b_tags[1].text.split(': ')[1]
    bonuses = b_tags[3].text.split(': ')[1]

    # Write to the SQLite database
    c.execute(f'UPDATE MapRecords SET Completions = ?, AverageTime = ?, Bonuses = ? WHERE MapName = ?',
              (completions, average_time, bonuses, map_name))

    # time.sleep(2)  # To prevent too frequent requests

# Commit the changes and close the connection
conn.commit()
conn.close()