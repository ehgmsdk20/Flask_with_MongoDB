Simple Blog
===========
Tech Stack Used: FLASK, MongoDB, HTML, CSS     
Prerequisite: MongoDB, Python

# 1. Description
This project was created by referring to the Flask tutorial documentation on the Flask official site(https://flask.palletsprojects.com/).   
I used mongoDB instead of sqlite, and implemented the login/logout function through flask_login library instead of session and g.   
Also, I added unregister function.   

# 2. How to use
You can download my project through the command.   
```
https://github.com/ehgmsdk20/Flask_with_MongoDB.git           
```
Then, create venv and activate the virtual environment.(available from Python 3.3 or higher)   
```
python -m venv venv           
venv/Scripts/activate         
```
Install the libraries for this project.   
```
pip install -r requirements.txt        
```     
Finally, run the Flask web application.   
```     
$env:FLASK_APP = "flaskr"           
flask run        
```   
