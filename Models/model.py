from site import ENABLE_USER_SITE
import sqlite3
con = sqlite3.connect('projeto.db')
cur = con.cursor()

def checkUser(username, password):
        cur.execute(f"SELECT * FROM Users WHERE username='{username}' AND password='{password}'")
        if cur.fetchone() != None:
            return True
        else:
            return False

def checkAdmin(username, password):
    cur.execute(f"SELECT role FROM Users WHERE username='{username}' AND password='{password}'")
    if cur.fetchone()[0] == "admin":
        return True
    else:
        return False
    
