import sqlite3

# Create a SQLite connection to 'export/surf_db.db'
conn = sqlite3.connect('export/surf_db.db')
c = conn.cursor()

# Add new columns to the MapTimes table for the headers in the Records table
c.execute("ALTER TABLE MapTimes ADD COLUMN MapTier INTEGER")
c.execute("ALTER TABLE MapTimes ADD COLUMN WRTime INTEGER")
c.execute("ALTER TABLE MapTimes ADD COLUMN WRHolder TEXT")
c.execute("ALTER TABLE MapTimes ADD COLUMN Completions INTEGER")
c.execute("ALTER TABLE MapTimes ADD COLUMN AverageTime INTEGER")
c.execute("ALTER TABLE MapTimes ADD COLUMN Bonuses INTEGER")

# Update the new columns in the MapTimes table with the values from the Records table
c.execute("""
    UPDATE MapTimes
    SET MapTier = Records.MapTier, 
        WRTime = Records.WRTime,
        WRHolder = Records.WRHolder,
        Completions = Records.Completions,
        AverageTime = Records.AverageTime,
        Bonuses = Records.Bonuses
    FROM Records 
    WHERE MapTimes.MapName = Records.MapName
""")

# Commit the changes and close the connection
conn.commit()
conn.close()