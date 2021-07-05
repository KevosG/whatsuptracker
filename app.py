import sqlite3, beepy, time
from sqlite3 import Error
from datetime import datetime, timedelta
from pathlib import Path

db_path = Path("./whatsup.db")
database = r"whatsup.db"

if db_path.is_file():
    pass
else:
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute('''CREATE TABLE ENTRIES
                ([Date] date,[Activity] text)''')

def top_menu():
    choice = input("Enter a selection.\n\n[1] - Start Timer\n[2] - View Entries\n[3] - Clear Entries\n[4] - Quit\n\n> ")
    if choice == "1":
        configure_timer()
    if choice == "2":
        entries = get_posts()
        for row in entries:
            print(row)
        top_menu()
    if choice == "3":
        clear_posts()
        top_menu()
    if choice == "4":
        quit()

def configure_timer():
    interval = int(input("How often to prompt? Press Enter to accept default of once every 20 minutes.\n\n[20] >") or "20")
    duration = int(input("For how many hours do you want to do this to yourself?  Press Enter to accept default of 2 hours. \n\n[2] >") or "2")
    print(f"Prompting every { interval } minutes for { duration } hours.")
    run_timer(duration, interval)

def run_timer(duration, interval):
    conn = create_connection(database)
    stop_time = datetime.now() + timedelta(hours=duration)
    while datetime.now() < stop_time:
        with conn:
            status_update = get_status()
            update_entries(conn, status_update)
        entries = get_posts()
        for row in entries:
            print(row)
        time.sleep(interval * 60)

def get_status():
    now = datetime.now()
    formatted_now = now.strftime("%m/%d/%Y, %H:%M")
    try:
        beepy.beep(sound = "coin")
    except:
        pass
    update = input("What have you been doing for the last 20 minutes?\n\n> ")
    status_update = (formatted_now, update)
    return status_update

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def get_posts():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute('select * from entries')
    posts = cur.fetchall()
    return posts

def clear_posts():
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute('DELETE FROM entries')
    conn.commit()

def update_entries(conn, status_update):
    sql = ''' INSERT INTO entries(date,activity)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, status_update)
    conn.commit()
    return cur.lastrowid

if __name__ == '__main__':
    top_menu()