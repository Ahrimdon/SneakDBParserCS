from bs4 import BeautifulSoup
import csv
import sqlite3
import requests
import os
# import shutil

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

# Check if surf_db.html exists
if os.path.isfile('temp/surf_db.html'):
    # Ask the user if they want to use the existing file
    use_existing = input("The file 'surf_db.html' already exists. Do you want to use this file? (y/N) ")
    if use_existing.lower() == 'y':
        # Open the HTML file and parse it with BeautifulSoup
        with open("temp/surf_db.html", 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    else:
        # Prompt the user for the webpage URL
        url = input("Please enter the URL of the of your profile for Sneak's database (e.g. https://snksrv.com/surfstats/?view=profile&id=STEAMID): ")

        # Fetch the webpage
        response = requests.get(url)

        # Save the webpage as surf_db.html
        with open('temp/surf_db.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

        # Call the check_or_create_directories function
        check_or_create_directories()

        # Parse it with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
else:
    # Prompt the user for the webpage URL
    url = input("Please enter the URL of the of your profile for Sneak's database (e.g. https://snksrv.com/surfstats/?view=profile&id=STEAMID): ")

    # Fetch the webpage
    response = requests.get(url)

    # Save the webpage as surf_db.html
    with open('temp/surf_db.html', 'w', encoding='utf-8') as f:
        f.write(response.text)

    # Call the check_or_create_directories function
    check_or_create_directories()

    # Parse it with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Open the HTML file and parse it with BeautifulSoup
with open("temp/surf_db.html", 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find the tables in the HTML
tables = soup.find_all('table', class_="table table-striped table-hover sortable")

# Define the headers for the CSV files
headers_map_records = ["Map Name", "Rank", "Best Time", "Date", "Start Speed"]
headers_map_times = ["Map Name", "Rank", "Personal Best", "Date", "Start Speed"]
headers_bonus_times = ["Map Name", "Personal Best", "Rank", "Bonus", "Date", "Start Speed"]

# Ask user for data output format
output_format = input("Do you want to save as 1) CSV, 2) SQLite DB, or 3) Both? ")

# Create a SQLite connection and overwrite tables if they exist
if output_format in ['2', '3']:
    conn = sqlite3.connect('export/surf_db.db')
    c = conn.cursor()

    # Delete the tables if they already exist in the SQLite database
    c.execute('''DROP TABLE IF EXISTS MapRecords;''')
    c.execute('''DROP TABLE IF EXISTS MapTimes;''')
    c.execute('''DROP TABLE IF EXISTS BonusTimes;''')

    # Create tables in the SQLite database
    c.execute('''CREATE TABLE MapRecords
                 (MapName text, Rank integer, BestTime text, Date text, StartSpeed text)''')

    c.execute('''CREATE TABLE MapTimes
                 (MapName text, Rank integer, PersonalBest text, Date text, StartSpeed text)''')

    c.execute('''CREATE TABLE BonusTimes
                 (MapName text, PersonalBest text, Rank integer, Bonus integer, Date text, StartSpeed text)''')

csv_writers = {}

# Parse the tables and write the data to CSV files and the SQLite database
for idx, table in enumerate(tables):
    # Define the CSV file and SQLite table to write to based on the table index
    if idx == 0:
        csv_file = 'map_records.csv'
        headers = headers_map_records
        table_name = 'MapRecords'
    elif idx == 1:
        csv_file = 'map_times.csv'
        headers = headers_map_times
        table_name = 'MapTimes'
    else:
        csv_file = 'bonus_times.csv'
        headers = headers_bonus_times
        table_name = 'BonusTimes'

    # Write to the CSV file
    if output_format in ['1', '3']:
        f = open('export/' + csv_file, 'w', newline='', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(headers)
        csv_writers[csv_file] = (f, writer)

    # Find all rows in the table
    rows = table.find_all('tr')

    # Loop through each row
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        
        # Check if the table is MapRecords and modify Rank to '1'
        if idx == 0:  # This is the MapRecords table
            cols[1] = '1'  # Change Rank to '1'

        # Write to the CSV file and SQLite database
        if output_format in ['1', '3']:
            csv_writers[csv_file][1].writerow(cols)
        if output_format in ['2', '3']:
            if table_name == 'BonusTimes':
                c.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)", cols)
            else:
                c.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?)", cols)


if output_format in ['2', '3']:
    # Commit the changes to the SQLite database
    conn.commit()
    # Close the SQLite connection
    conn.close()
#   shutil.copy2('export/surf_db.db', 'sqlite_web_viewer/database/surf_db.db') # Not needed with new batch format

# Close the CSV files
for f, writer in csv_writers.values():
    f.close()

# Extract general stats
general_stats = soup.find('h2').text.strip() + "\n"
general_stats += soup.find('h2').next_sibling.strip() + "\n"
general_stats += soup.find('b').text.strip() + "\n\n"

stat_table = soup.find('table', class_="table table-striped table-hover")
rows = stat_table.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    general_stats += " | ".join(cols) + "\n"

with open('export/general_stats.log', 'w', encoding='utf-8') as f:
    f.write(general_stats)