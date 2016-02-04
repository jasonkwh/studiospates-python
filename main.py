__author__ = 'Hanxiang Huang'

from bottle import Bottle, template, static_file, request, response
import interface
from database import COMP249Db
from users import check_login, session_user, delete_session, generate_session
import datetime

application = Bottle()

@application.route('/')
def index():
    """Index of Psst site"""
    db = COMP249Db()
    username = session_user(db)
    loginString = ""
    content = ""
    http = ""
    str = ""
    avatar = ""
    list = interface.post_list(db, usernick=None, limit=50)

    # if user not logged in
    if not username:
        # display input field for username and password if the user not logged in
        loginString = "<h3>member login</h3><br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"

    # if user logged in
    if username:
        avatar = interface.user_avatar(db,username)
        # display the input field for adding posts instead of the title
        str = str + "<form action='/post' id='postform' method='POST'><input type='postfield' name='post' placeholder='post content, formats: [i]image urls[/i][t]title[/t][p]contents[/p]#tags #tags2' value='[i]image urls[/i][t]title[/t][p]contents[/p]#tags #tags2' class='focus' onKeyPress='return submitenter(this,event)'></form>"
        loginString = "<a href='/users/" + username + "'><img src='" + avatar + "'><h3 style='text-align:center; margin-left:0px;'>" + username + "</h3></a><br><form action= '/logout' id='logoutform' name='logoutform' method='POST' ><input type='submit' value='logout' class='sun-flower-button'></form>"

    for item in list:
        content = interface.post_to_html(item[3])
        http = interface.post_to_html(content)
        dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
        str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display

    return template('base.tpl', base=str, validate='', login=loginString)


@application.post('/login')
def login():
    """Display this page if any invalid user identification"""
    db = COMP249Db()
    list = interface.post_list(db, usernick=None, limit=50)
    content = ""
    http = ""
    str = ""

    # display previous posts
    for item in list:
        content = interface.post_to_html(item[3])
        http = interface.post_to_html(content)
        dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
        str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display

    # if there are something within the login field...
    if 'nick' in request.forms:
        username = request.forms['nick'] # get username from the 'nick' field
        password = request.forms['password'] # get password from the 'password' field
        str2 = "<p style='color:red;font-size:small;'>Invaild username or password</p>"
        loginString = "<h3>member login</h3></br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"
        if not check_login(db, username, password):
            return template('base.tpl', base=str, validate=str2, login=loginString) # display 'Failed' if invaild user identification
        generate_session(db, username) # generate the user session
        response.set_header('Location', '/')
        response.status = 303
        return "Redirect to /" # redirect to /


@application.post('/logout')
def logout():
    """Logout"""
    db = COMP249Db()
    username = session_user(db) # retrieve user session information from the database
    if username:
        delete_session(db, username) # remove user session
        response.set_header('Location', '/')
        response.status = 303
        return "Redirect to /" # redirect to /

@application.post('/post')
def add_post():
    """Adding post"""
    db = COMP249Db()
    username = session_user(db) # retrieve user session information from the database
    if username:
        content = request.forms['post'] # get user inputs from the input form 'post'
        interface.post_add(db, username, content) # add post by post_add function of interface.py
        response.set_header('Location', '/')
        response.status = 303
        return "Redirect to /" # redirect to /

@application.post('/search')
def search():
    """Search feature, can search user name and / or contents"""
    db = COMP249Db()
    username = session_user(db) # retrieve user session information from the database
    loginString = ""
    content = ""
    http = ""
    avatar = ""

    if 'search' in request.forms:
        search = request.forms['search'] # get user inputs from the search field
        str = "<h2>Search results for '" + search + "':</h2>" # title
        list = interface.post_list(db, usernick=None, limit=50)
        if not username: # display the things below only if user not logged in
            # display input field for username and password if the user not logged in
            loginString = "<h3>member login</h3></br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"

        if username: # display the things below only if user logged in
            avatar = interface.user_avatar(db,username)
            loginString = "<a href='/users/" + username + "'><img src='" + avatar + "'><h3 style='text-align:center; margin-left:0px;'>" + username + "</h3></a><br><form action= '/logout' id='logoutform' name='logoutform' method='POST' ><input type='submit' value='logout' class='sun-flower-button'></form>"

        for item in list:
            content = interface.post_to_html(item[3])
            http = interface.post_to_html(content)
            dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
            dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
            if ((bool(search.lower() in item[2].lower())) | (bool(search.lower() in http.lower()))):
                str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display

        return template('base.tpl', base=str, validate='', login=loginString)

@application.route('/search=<searchThings>')
def search2(searchThings):
    """Search feature, can search user name and / or contents"""
    db = COMP249Db()
    username = session_user(db) # retrieve user session information from the database
    loginString = ""
    content = ""
    http = ""
    avatar = ""
    search = searchThings
    str = "<h2>Search results for '" + search + "':</h2>" # title
    list = interface.post_list(db, usernick=None, limit=50)

    if not username: # display the things below only if user not logged in
        # display input field for username and password if the user not logged in
        loginString = "<h3>member login</h3></br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"

    if username: # display the things below only if user logged in
        avatar = interface.user_avatar(db,username)
        loginString = "<a href='/users/" + username + "'><img src='" + avatar + "'><h3 style='text-align:center; margin-left:0px;'>" + username + "</h3></a><br><form action= '/logout' id='logoutform' name='logoutform' method='POST' ><input type='submit' value='logout' class='sun-flower-button'></form>"

    for item in list:
        content = interface.post_to_html(item[3])
        http = interface.post_to_html(content)
        dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
        if ((bool(search.lower() in item[2].lower())) | (bool(search.lower() in http.lower()))):
            str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display

    return template('base.tpl', base=str, validate='', login=loginString)


@application.route('/users/<username:path>')
def users(username):
    """Generate the webpage that displays the user posts"""
    db = COMP249Db()
    uname = session_user(db) # retrieve user session information from the database
    loginString = ""
    list2 = interface.post_list(db, usernick=None, limit=50)
    str = ""
    content = ""
    http = ""
    avatar = ""

    str = "<h2>" + username + "'s posts:</h2>" # title
    if not uname:
        # display input field for username and password if the user not logged in
        loginString = "<h3>member login</h3></br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"

    if uname:
        avatar = interface.user_avatar(db,uname)
        loginString = "<a href='/users/" + uname + "'><img src='" + avatar + "'><h3 style='text-align:center; margin-left:0px;'>" + uname + "</h3></a><br><form action= '/logout' id='logoutform' name='logoutform' method='POST' ><input type='submit' value='logout' class='sun-flower-button'></form>"

    for item in list2:
        if (username == item[2]): # display the post only if the username and the author is the same person
            content = interface.post_to_html(item[3])
            http = interface.post_to_html(content)
            dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
            dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
            str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display
    return template('base.tpl', base=str, validate='', login=loginString)


@application.route('/mentions/<username:path>')
def mentions(username):
    """Generate the webpage that displays @users"""
    db = COMP249Db()
    uname = session_user(db) # retrieve user session information from the database
    loginString = ""
    content = ""
    http = ""
    list = interface.post_list_mentions(db, usernick=username, limit=50)
    str = ""
    avatar = ""

    str = "<h2>Posts mentioned " + username + ":</h2>" # title
    if not uname:
        # display input field for username and password if the user not logged in
        loginString = "<h3>member login</h3></br><form id='loginform' method='POST' action ='/login'><input type='text' name='nick' placeholder='username' class='focus' onKeyPress='return submitenter(this,event)'><input type='password' name='password' placeholder='password' class='focus' onKeyPress='return submitenter(this,event)'></form>"

    if uname:
        avatar = interface.user_avatar(db,uname)
        loginString = "<a href='/users/" + uname + "'><img src='" + avatar + "'><h3 style='text-align:center; margin-left:0px;'>" + uname + "</h3></a><br><form action= '/logout' id='logoutform' name='logoutform' method='POST' ><input type='submit' value='logout' class='sun-flower-button'></form>"

    for item in list:
        content = interface.post_to_html(item[3])
        http = interface.post_to_html(content)
        dt = datetime.datetime.strptime(item[1],"%Y-%m-%d %H:%M:%S")
        dt_string = dt.strftime("%b %d, %Y %I:%M%p").upper()
        str = str + "<div class='entry'><a href='/users/" + item[2] + "'><div class='item'><img src='" + item[4] + "'> <p>" + item[2].upper() + "</p></div></a><div class='date'><p>" + dt_string + "</p></div>" + http + "<hr></div>" # contents display

    return template('base.tpl', base=str, validate='', login=loginString)


@application.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


if __name__ == '__main__':
    application.run(host='localhost', port=8080, debug=True)