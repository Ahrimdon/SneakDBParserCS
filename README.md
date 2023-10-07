# SneakDBParserCS

![image](assets/SneaksCommunity.png)

## Table of Contents

- [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Supported Gamemodes](#supported-gamemodes)
  - [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Finding Your SteamID](#finding-your-steamid)
- [Instructions](#instructions)
    - [**Command Line Arguments**](#command-line-arguments)
    - [**Using the Python Script**](#using-the-python-script)
  - [Example](#example)
- [Credits](#credits)
- [License](#license)

### Introduction
-----
SneakDBParserCS is a highly-efficient Python script designed to help you organize and manage your Counter-Strike surf times. This tool lets you extract your database information from Sneak's Counter-Strike Database conveniently via an HTML file. It offers two distinct methods for exporting your data, as *Comma Separated Values (**.csv**)* files, and as a *SQLite Database (**.db**)*. With SneakDBParserCS, viewing and analyzing your surf times has never been easier!

### Features
-----
- **Web Scraping**: The script uses BeautifulSoup to scrape the parse data from the user's Sneak's Counter-Strike Database profile.
- **Data Parsing**: It accurately parses the scraped data into usable information such as Map Records, Map Times, Map Tier, and Bonus Times, and more!
- **Dynamic Data Export**: The script provides an option to export the parsed data into various formats such as CSV and SQLite Database, or both. 
- **Local Webfront**: Allows the user to locally host a WebGUI to display, modify and query their database!

### Supported Gamemodes
-----
- **CS:GO Surf**

### Prerequisites
-----
Before you begin, ensure you have met the following requirements:
* You have a `Windows` machine running [Python 3.9](https://www.python.org/downloads/) or later.
  * When installing, check-marking the box `ADD TO PATH` is recommended.

* If you are on `Windows` and do not have Python installed, you can use the provided executable - `SneakDBParser.exe`

## Installation
- Download the ZIP archive or clone the repository `git clone https://github.com/Ahrimdon/SneakDBParserCS.git && cd SneakDBParserCS`
- Run the setup using the command `setup.py`.

## Finding Your SteamID
1. Make sure your Steam profile is set to public
2. Right-click on profile --> `Copy Page URL`
3. Enter the URL into the [SteamID Finder](https://steamid.io/lookup/76561198092410085) (e.g. `STEAM_1:1:66072178`)

## Instructions

#### **Command Line Arguments**
```
  -h, --help           show this help message and exit
  --steam_id STEAM_ID  The Steam ID to be used
  --update             Update the surf profile
  --build              Build or update the database
  --parse              Parse the database
  --complete           Run --update, --build, and --parse consecutively
```

> For example, to build the the complete database with you surf statistics you can use `./SneakDBParser.exe --steam_id STEAM_1:1:66072178 --complete`

**This will pull your surf stats, build the database, and parse the results.**

-----

#### **Using the Python Script**
1. **Step 1:** Navigate to the repository using `cd SneakDBParserCS`.

2. **Step 2:**  Run `main.py`, select `1` and enter your SteamID (e.g. STEAM_1:1:66072178).
   
  > ***Note:*** If you already have a `surf_db.html` it will first ask if you wish to use it or overwrite it.

3. **Step 3:** Choose what you wish to save your Database entries as `(.csv, .db, both)`.

4. **Step 4:** Run `main.py` and select `2` to build the initial database.

  > ***Note:*** It is only necessary to build the initial database *once* during first installation, or when updating the database.

5. **Step 5:** Your DB entries will then be saved in a folder named `export`.

6. **Step 6:** Run `main.py` and select `3` to parse the all of the general entries into your own. 

7. **Step 7 (Optional):** To view, query, and sort your database with ease, run the batch file `StartWebfront.bat`. To see your database, visit `http://127.0.0.1:7890/` or `http://localhost:7890/`. From here you can view, sort, query entries and ***much*** more!.

<u>**All actions above work with double-clicking the provided executable**</u>
### Example
-----
![image](assets/Example.png)

## Credits
- Creator - **Ahrimdon**

- Main Tester - **PandaMane**

## License
Distributed under the MIT License. See `LICENSE` for more information.