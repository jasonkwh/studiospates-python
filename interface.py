"""
@author: Hanxiang Huang (Jason)
"""

from database import COMP249Db
import re

db = COMP249Db()

def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""
    content = content.replace("Ã¢","â") # temporary conversion for â
    content = content.replace("[i]", "<img src='")
    content = content.replace("[/i]", "' class='mimage'>")
    content = content.replace("[t]", "<h4>")
    content = content.replace("[/t]", "</h4>")
    content = content.replace("[p]", "<p>")
    content = content.replace("[/p]", "</p><br>tags: ")
    content = content.replace("& ", "&amp; ") # replace '& ' with '&amp; '
    at_re = r'(@)([\w\./]*)' # use regex to find mentions (e.g., @Mandible)
    replace_string2 = '<a href=' + "'/users/\\2'" + '>' + "\\1\\2" + '</a>' # convert user mentions to html code
    content = re.sub(at_re, replace_string2, content) # change the content as a link
    sharp_re = r'(#)([\w\./]*)' # use regex to find tags (e.g., #tags)
    replace_string3 = '#<a href=' + "'/search=\\2'" + '>' + "\\2" + '</a>' # convert user mentions to html code
    content = re.sub(sharp_re, replace_string3, content)
    content = content.replace(".'>", "'>") # fix some error for special situations...
    content = content.replace(".</a>", "</a>.") # fix some error for special situations...
    return content


def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar, content)
    """
    li = []
    cur = db.cursor()
    loop = 0
    if(usernick==None): # return all posts if usernick is none
        # retrieve data from the database
        row = list(cur.execute("SELECT id, timestamp, usernick, content, users.avatar FROM posts, users WHERE users.nick = posts.usernick ORDER BY timestamp DESC"))
        for item in row:
            if loop < limit: # limits the posts display
                loop = loop + 1
                li.append(item)
        return li

    elif(usernick!=None): # return all posts of the user
        # retrieve data from the database
        row = list(cur.execute("SELECT id,timestamp, usernick, content, users.avatar FROM posts, users WHERE usernick =? AND posts.usernick = users.nick ORDER BY timestamp DESC",(usernick,)))
        for item in row:
            if loop < limit: # limits the posts display
                loop = loop + 1
                li.append(item)
        return li



def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """
    li = []
    cur = db.cursor()
    # retrieve data from the database
    row = list(cur.execute("SELECT id, timestamp, usernick, content, users.avatar FROM posts, users WHERE users.nick = posts.usernick ORDER BY timestamp DESC"))
    loop = 0
    for item in row:
        if loop < limit: # limits the posts display
            loop = loop + 1
            if(item[3].find(usernick)!=-1): # add to the list only if the usernick is exist within the post content
                li.append(item)
    return li


def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""

    if(len(message) < 551): # 551 words limits
        cur = db.cursor()
        cur.execute("INSERT INTO posts (usernick, content) VALUES(?,?)", (usernick, message,)) # add stuffs into the database
        db.commit()
        row = list(cur.execute("SELECT id, timestamp, usernick, content, users.avatar FROM posts, users WHERE users.nick = posts.usernick ORDER BY timestamp DESC"))
        return row[0][0] # retrieve the id of the post
    else:
        return None


def user_avatar(db, usernick):
    cur = db.cursor()
    row = cur.execute("SELECT nick, avatar FROM users WHERE nick=?", (usernick,))
    for item in row:
        return item[1]
