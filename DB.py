import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()

# cur.execute('''CREATE TABLE Users IF NOT EXISTS(
#            id INT PRIMARY KEY AUTOINCREMENT,
#            user_id TEXT NOT NULL,
#            password TEXT NOT NULL
#  ); ''')

# cur.execute(''' INSERT INTO Users (id, user_id, password)
# VALUES (2, 'brftester', 'brftester'); ''')
# cur.execute(''' INSERT INTO Users (id, user_id, password)
# VALUES (1, 'brfadmin', 'brfadmin'); ''')

# con.commit()
# user = 'brftester'

# cur.execute('''CREATE TABLE Endpoints(
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            endpoint TEXT NOT NULL,
#            server_type TEXT NOT NULL,
#            environment TEXT NOT NULL
#  ); ''')

# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.google.com', 'Realtime', 'DIF'); ''')
#
# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.youtube.com', 'Realtime', 'DIF'); ''')
#
# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.google.com', 'Realtime', 'SE'); ''')
#
# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.youtube.com', 'Realtime', 'SE'); ''')
#

# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.youtube.com', 'online', 'DIF'); ''')
#
# cur.execute(''' INSERT INTO Endpoints (endpoint, server_type, environment)
# VALUES ('https://www.youtube.com', 'online', 'SE'); ''')
#
# con.commit()

# rows = cur.execute('''SELECT * FROM Endpoints WHERE server_type=? AND environment=?''',
#                                   ('online', 'DIF')).fetchall()

rows = cur.execute('''SELECT endpoint FROM Endpoints WHERE server_type=? AND environment=?''',
                            ('online', 'DIF')).fetchall()
for row in rows:
    print(row)