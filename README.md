# BeanBlog by coolbeans
# Roster: 
  TNPG         : coolbeans

  Evan Chan    : Project Manager

  Amanda Tan   : Middleware

  Danny Mok    : Frontend

  Michelle Zhu : Database
  
To install, go to the top of the page and click the green button that says "Code". In the dropdown that appears, click "Download Zip" at the bottom.

To clone the repository, go to the top of the page and click the green button that says "Code". In the dropdown that appears, choose either "HTTPS" or "SSH" under the "Clone" section and copy the provided URL. Open up your computer's terminal and type "git clone {URL HERE}"
Launch Codes:

# Project Description: 
  A blog website that is capable of allowing logged-in users to view and create blog posts. 
  ```
  Users:
  
    - Have a feed of all posts, sorted by most recent at the top
    - View others' posts
    - Create and edit own posts 

  Site Services:

    - SQLite database of posts and user info
    - Templates and CSS for site consistency
    - Table for saved sessions to reduce login friction
  
```
  
# Install Guide:
  To install, go to the top of the page and click the green button that says "Code". In the dropdown that appears, click "Download Zip" at the bottom. Extract the zip from your downloads into your home directory. <br>

OR
  
  To clone the repository, go to the top of the page and click the green button that says "Code". In the dropdown that appears, choose either "HTTPS" or "SSH" under the "Clone" section and copy the provided URL. Open up your computer's terminal and type "git clone {URL HERE}"
# Launch Codes:
  Instructions:
  1. Make a python virtual environment

      a. Open up your device's terminal

      b. Type ```$ python3 -m venv {path name}``` or ```$ py -m venv {path name}```

      c. Type in one of the commands into your terminal for your specific OS to activate the environment

      - Linux: ```$ . {path name}/bin/activate```
    
      - Windows Command Prompt: ```> {path name}\Scripts\activate```

      - Windows PowerShell: ```> . .\{path name}\Scripts\activate```

      - MacOS: ```$ source {path name}/bin/activate```

      (If successful, the command line should display the name of your virtual environment: ```({path name})$ ```)

      d. When done, type ```$ deactivate``` to deactivate the virtual environment

  3. Ensure your virtual environment is activated

  4. Access the repository by typing ```$ cd coolbeans__evanc107_amandat109_dannym2789_jiayingz16```

  5. Type ```$ pip install -r requirements.txt``` to install the required modules

 - If terminal returns ```zsh: command not found: pip```, type ```$ pip3 install -r requirements.txt``` because ```$ pip``` is for python2.

  6. Type ```$ python3 app/app.py``` to run the application

  7. Copy / type "http://127.0.0.1:5000" or "http://localhost" onto a browser to view the website
