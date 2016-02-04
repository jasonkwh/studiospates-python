"""
@author: Hanxiang Huang (Jason)
"""

import bottle
import uuid

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'studiospates'

def check_login(db, usernick, password):
    """returns True if password matches stored"""

    cur = db.cursor()
    # retrieve user information from the database
    rows = cur.execute("SELECT nick, password FROM users")
    for item in rows:
        if(item[0] == usernick and item[1] == db.crypt(password)): # if the username and password match the database
            return True
        elif(item[0] == usernick and item[1] != db.crypt(password)): # if the username and/or password does not match
            return False


def generate_session(db, usernick):
    """create a new session and add a cookie to the request object (bottle.request)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """

    cur = db.cursor()
    rows = cur.execute("SELECT nick FROM users") # retrieve nick from users table
    for item in rows:
      if(item[0] == usernick): # if the sql entry exists
        rows = [row[0] for row in cur.execute("SELECT sessionid From sessions WHERE usernick = '%s'"%usernick)]
        if len(rows) == 0: # if the sessionid not exist
         sessionid = str(uuid.uuid4())
         cur.execute("INSERT INTO sessions VALUES(?,?)", (sessionid, usernick,)) # generate new session with the new ID
         db.commit()
         bottle.response.set_cookie(COOKIE_NAME, usernick) # set cookies
         return sessionid
        else:
         sessionid = rows[0] # if the sessionid is exist
         return sessionid
    else:
        return None



def delete_session(db, usernick):
    """remove all session table entries for this user"""

    bottle.response.set_cookie(COOKIE_NAME, '')
    cur = db.cursor()
    cur.execute("DELETE FROM sessions where usernick=?", (usernick,)) # remove user sessions entries within the database
    db.commit()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""

    if bottle.request.get_cookie(COOKIE_NAME) != '' or bottle.request.get_cookie(COOKIE_NAME) != None:
        cur = db.cursor()
        # retrieve user sessionid and usernick (username) from the sessions table
        rows = [row[0]for row in cur.execute("SELECT sessionid, usernick FROM sessions")]

        if(len(rows) == 0) : # if not exist
            return None
        else:
            return bottle.request.get_cookie(COOKIE_NAME)
    else:
        return None
