'''
Coolbeans: Evan, Michelle, Danny, Amanda
'''

#imports
from flask import Flask, redirect, render_template, session, request
import os

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.urandom(32)

#user login variables
userTable = False

logins = {
    "danny": "mok",
    "amanda": "tan",
    "evan": "chan",
    "michelle": "zhu"
}


@app.route('/')
def recoverSession():
    if 'username' in session:
        return redirect('/home')# goes directly to home if session is recovered
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def userLogin():
    print("")
    if 'username' in session:
        return redirect('/home')# go home if session is recovered

    if request.method == 'POST':
        login = request.form
        username = login.get('username')# get the user's user
        password = login.get('password')# get pw

        if not username or not password:#if user/pw is not filled out
            #we can change this later to say user/pw is missing rather than redirecting
            return redirect('/login')# go back to login if wrong

        if username in logins and logins[username] == password:# if user is in login, then if the key for username matches inputted pw
            session['username'] = username# saves user cookie, will use later to authenticate thru out diff pages
            return redirect('/home')  # render home
        else:
            return redirect('/login')# resets page if user exists but pw doesnt match
    return render_template("login.html")# if method not POST

@app.route('/home')
def displayHome():
    if 'username' not in session:
        return redirect('/login')# prevents people from getting in by changing url
    return render_template("home.html")

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == "__main__": #false if this file imported as module
    app.debug = True
    app.run()
