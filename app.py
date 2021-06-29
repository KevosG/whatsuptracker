


# # Create database if it doesn't exist, need to add conditional later
# conn = sqlite3.connect('whatsup.db')
# c = conn.cursor()
# c.execute('''CREATE TABLE ENTRIES
#              ([Date] date,[Activity] text)''')


#  MENU
# 1 - Start timer
#   1a - How often to prompt?
#   1b - How long to prompt for?
# 2 - View Entries
#   2a - Today Only
#   2b - All Entries
# 3 - Export to CSV
# 3 - Clear Entries
#   3a - Are you sure?
# 4 - Quit

import sqlite3, beepy
from sqlite3 import Error
from datetime import datetime
import time

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def get_posts(conn):
    cur = conn.cursor()
    cur.execute('select * from entries')
    posts = cur.fetchall()

    return posts

def update_entries(conn, status_update):
    sql = ''' INSERT INTO entries(date,activity)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, status_update)
    conn.commit()

    return cur.lastrowid

def get_status():
    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y, %H:%M")
    beepy.beep(sound = "coin")
    update = input("What have you been doing for the last 20 minutes?\n\n--> ")
    status_update = (formatted_now, update)

    return status_update

def main():
    while True:
        database = r"whatsup.db"
        conn = create_connection(database)
        with conn:
            status_update = get_status()
            update_entries(conn, status_update)
        entries = get_posts(conn)
        for row in entries:
            print(row)
        time.sleep(1200)

if __name__ == '__main__':
    main()
