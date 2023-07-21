from bs4 import BeautifulSoup
import csv
import sqlite3
import requests
import os
import time
# import shutil

def prompt_user_choice():
    print("Select an option:")
    print("1) Update your surf profile")
    print("2) Build/Update the database")
    print("3) Parse the database")
    choice = input("Enter your choice: ")
    return choice

def update_surf_profile():
    # Check if the 'temp' directory exists. If not, create it. We want this created before everything else.
    if not os.path.exists('temp'):
        os.makedirs('temp')

    def check_or_create_directories():
        # Check if the 'export' directory exists. If not, create it.
        if not os.path.exists('export'):
            os.makedirs('export')

    # Check if surf_db.html exists
    if os.path.isfile('temp/surf_db.html'):
        # Ask the user if they want to use the existing file
        use_existing = input("The file 'surf_db.html' already exists. Do you want to use this file? (y/N) ")
        if use_existing.lower() == 'y':
            # Open the HTML file and parse it with BeautifulSoup
            with open("temp/surf_db.html", 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
        else:
            # Prompt the user for their Steam ID
            steam_id = input("Please enter your Steam ID: ")

            # Build the URL
            url = f"https://snksrv.com/surfstats/?view=profile&id={steam_id}"

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
        # Prompt the user for their Steam ID
        steam_id = input("Please enter your Steam ID: ")

        # Build the URL
        url = f"https://snksrv.com/surfstats/?view=profile&id={steam_id}"

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
                    (MapName TEXT, Rank INTEGER, BestTime TEXT, Date TEXT, StartSpeed TEXT)''')

        c.execute('''CREATE TABLE MapTimes
                    (MapName TEXT, Rank INTEGER, PersonalBest TEXT, Date TEXT, StartSpeed TEXT)''')

        c.execute('''CREATE TABLE BonusTimes
                    (MapName TEXT, PersonalBest TEXT, Rank INTEGER, Bonus INTEGER, Date TEXT, StartSpeed TEXT)''')

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

def build_database():
    # Check if the 'temp' directory exists. If not, create it.
    if not os.path.exists('temp'):
        os.makedirs('temp')

    def check_or_create_directories():
        # Check if the 'export' directory exists. If not, create it.
        if not os.path.exists('export'):
            os.makedirs('export')

    # Fetch the webpage
    url = "https://snksrv.com/surfstats/?view=maps"
    response = requests.get(url)

    # Parse it with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if MapDB.html exists
    if not os.path.isfile('temp/MapDB.html'):
        # Save the webpage as MapDB.html
        with open('temp/MapDB.html', 'w', encoding='utf-8') as f:
            f.write(response.text)

    # Call the check_or_create_directories function
    check_or_create_directories()

    # Find the tables in the HTML
    table = soup.find('table', class_="table table-striped table-hover sortable")

    # Create a SQLite connection to 'export/surf_db.db' and overwrite table if it exists
    conn = sqlite3.connect('export/surf_db.db')
    c = conn.cursor()

    # Delete the table if it already exists in the SQLite database
    c.execute('''DROP TABLE IF EXISTS Records;''')

    # Create tables in the SQLite database
    c.execute('''CREATE TABLE Records
                    (MapName TEXT, MapTier INTEGER, WRTime INTEGER, WRHolder TEXT,
                    Completions INTEGER, AverageTime INTEGER, Bonuses INTEGER)''')

    # Write to the SQLite database
    for row in table.findAll('tr'):
        columns = row.findAll('td')
        values = [col.text.strip() for col in columns]
        if values:
            # Write to the SQLite database
            c.execute(f'INSERT INTO Records (MapName, MapTier, WRTime, WRHolder) VALUES (?, ?, ?, ?)', values)

    conn.commit()  # Commit after all inserts

    # Create a new cursor for fetching data
    c2 = conn.cursor()

    # Fetch additional data
    for row in c2.execute('SELECT MapName FROM Records WHERE Completions IS NULL'):
        map_name = row[0]
        url = f"https://snksrv.com/surfstats/?view=map&name={map_name}"
        # Ask the user if they want to download all map info
        # download = input(f"Do you want to download additional map information? (y/N) ")
        # if download.lower() != 'y':
        #     continue

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        subheader = soup.find('div', class_='subheader')
        b_tags = subheader.find_all('b')

        completions = b_tags[0].text.split(': ')[1]
        average_time = b_tags[1].text.split(': ')[1]
        bonuses = b_tags[3].text.split(': ')[1]

        # Write to the SQLite database
        c.execute(f'UPDATE Records SET Completions = ?, AverageTime = ?, Bonuses = ? WHERE MapName = ?',
                (completions, average_time, bonuses, map_name))

        # time.sleep(2)  # To prevent too frequent requests

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Ask user if they want to export data to CSV files
    output_to_csv = input("Do you want to export data to CSV files? (y/N) ")
    if output_to_csv.lower() == 'y':
        # Add the code to export data to CSV files

def parse():
    # Create a SQLite connection to 'export/surf_db.db'
    conn = sqlite3.connect('export/surf_db.db')
    c = conn.cursor()

    # Create a new table MapTimesTemp with the updated structure
    c.execute("""
        CREATE TABLE MapTimesTemp
        (
            MapName TEXT, 
            Rank INTEGER, 
            PersonalBest TEXT, 
            Date TEXT, 
            StartSpeed TEXT,
            MapTier INTEGER,
            WRTime INTEGER,
            WRHolder TEXT,
            Completions INTEGER,
            AverageTime INTEGER,
            Bonuses INTEGER
        )
    """)

    # Copy the data from the MapTimes and Records tables to MapTimesTemp
    c.execute("""
        INSERT INTO MapTimesTemp (MapName, Rank, PersonalBest, Date, StartSpeed, MapTier, WRTime, WRHolder, Completions, AverageTime, Bonuses)
        SELECT 
            MapTimes.MapName, 
            MapTimes.Rank, 
            MapTimes.PersonalBest, 
            MapTimes.Date, 
            MapTimes.StartSpeed,
            Records.MapTier, 
            Records.WRTime, 
            Records.WRHolder, 
            Records.Completions, 
            Records.AverageTime, 
            Records.Bonuses
        FROM MapTimes
        LEFT JOIN Records ON MapTimes.MapName = Records.MapName
    """)

    # Drop the old MapTimes table
    c.execute("DROP TABLE MapTimes")

    # Rename MapTimesTemp to MapTimes
    c.execute("ALTER TABLE MapTimesTemp RENAME TO MapTimes")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def main():
    user_choice = prompt_user_choice()
    if user_choice == '1':
        update_surf_profile()
    elif user_choice == '2':
        build_database()
    elif user_choice == '3':
        parse()
    else:
        print("Invalid input! Please enter either '1', '2' or '3")

if __name__ == "__main__":
    main()