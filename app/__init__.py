'''
Coolbeans: Evan, Michelle, Danny, Amanda
'''

#imports
from flask import Flask, redirect, render_template, session, request
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

#user login variables
loggedIn = False
userTable = False







@app.route('/')
def recover():
    if 'username' in session:
        loggedIn = True
        return redirect('/home')# Goes directly to home if session is recovered
    return redirect('/login')# Goes to login page if not

@app.route('/login')
def gate():
    return render_template(login.html)
# @app.route('/signup')
#
# @app.route('/home')
#
# @app.route('/create')
#
# @app.route('/view')
#
# @app.route('/edit')
#
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__': #false if this file imported as module
    app.debug = True
    app.run()
