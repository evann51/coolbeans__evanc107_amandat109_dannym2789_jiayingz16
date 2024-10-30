"""
Coolbeans: Evan, Michelle, Danny, Amanda
"""

#imports
from flask import Flask, redirect
app = Flask(__name__)

#user login variables
loggedIn = false
userTable =







@app.route("/")
def recover():
    if loggedIn:
        redirect("/login")

@app.route("/login")

@app.route("/signup")

@app.route("/home")

@app.route("/create")

@app.route("/view")

@app.route("/edit")

@app.route("/logout")

if __name__ == "__main__":
    app.debug = True        
    app.run()
