# SneakDBParserCS

![image](assets/SneaksCommunity.png)

## Table of Contents

- [SneakDBParserCS](#SneakDBParserCS)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#Installation)
  - [Instructions](#instructions)
  - [License](#license)

## Introduction
SneakDBParserCS is a highly-efficient Python script that enables you to organize and manage your Counter-Strike surf times. This tool lets you extract your database information from Sneak's Counter-Strike Database conveniently via an HTML file. It offers two distinct methods for exporting your data, as *Comma Separated Values (**.csv**)* files, and as a *SQLite Database (**.db**)*. With SneakDBParserCS, viewing and analyzing your surf times has never been easier!

## Features
- **Web Scraping**: The script uses BeautifulSoup to scrape the data from the user's Sneak's Counter-Strike Database profile.
- **Data Parsing**: It accurately parses the scraped data into usable information such as Map Records, Map Times, and Bonus Times.
- **Dynamic Data Export**: The script provides an option to export the parsed data into various formats such as CSV and SQLite Database, or both. 
- **Automated Directory Management**: It automatically checks for necessary directories and creates them if not already present.
- **User-Interaction**: It allows the user to interact at various points like choosing between existing file or fetching the fresh file, selecting the data export format, etc. 

## Supported Gamemodes
- **CS:GO Surf**

## Prerequisites
Before you begin, ensure you have met the following requirements:
* You have a `Windows` machine running [Python 3.5](https://www.python.org/downloads/) or later.
  * When installing, check-marking the box `ADD TO PATH` is recommended.

## Installation

1.  * Download the latest release (.exe or .py)
     <br>
     **OR**
     <br>
    * Clone the repository using `git clone https://github.com/Ahrimdon/SneakDBParserCS.git`

2. Navigate to the directory using `cd SneakDBParserCS`

3. Run the setup using the command `setup.py`

## Instructions
Follow the steps below to use the SneakDBParserCS:

#### **Using the Python Script**
1. **Step 1**: Navigate to the repository using `cd SneakDBParserCS`

2. **Step 2**: Execute `run.py` and enter the URL to your profile for SneakSrvDB (e.g. https://snksrv.com/surfstats/?view=profile&id=YOURSTEAMID)

3. **Step 3**: Choose what you wish to save your Database entries as `(.csv, .db, both)`

    *If you already have a `surf_db.html` it will first ask if you wish to use it or overwrite it

4. **Step 4**: Your DB entries will then be saved in a folder named `export`

5. **Step 5 (Optional)**: To view, query, and sort your database with ease, run the batch file `StartWebfront.bat`. To see your database, visit `http://127.0.0.1:7890/` or `http://localhost:7890/`. From here you can view, sort, query entries and ***much*** more!

## License
Distributed under the MIT License. See `LICENSE` for more information.
