import os, jinja2

from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename


global app
app = Flask(__name__, template_folder='menu/templates/')
app.secret_key = 'secret'

#def registerBlueprints(app):
#from menu.services import menu
#app.register_blueprint(menu, url_prefix='/menu')


#################### connect to database ###############
#!/usr/bin/python
import mysql.connector as mariadb
db = mariadb.connect(user='root', password='123', database='cc_manager')
  #username for database, password, databasename
cursor = db.cursor()


#################### index page ################
@app.route('/')            #starting page
def index():
    return render_template('login.html')


#################  login     ##############
@app.route('/login', methods=['POST'])       #on submission of login details
def login():   
    global user
    user = str(request.form['Username'])
    passwd = str(request.form['Password'])
          
    sql = "SELECT * FROM user \
          WHERE username = '%s'" % (user)       #checking if user is already there in database
    try:  
      cursor.execute(sql)
      results = cursor.fetchall()
      print results
      
      if results == []:
         return render_template('contact_admin.html')
      elif results[0][2]  != passwd:  
         return render_template('alert_login.html')      #if wrong password
      else:
         print "register"
         #registerBlueprints(app)
         return redirect(url_for('show_menu'))            
    except:
      print "not ok"  
    print "username: ", user      
    return render_template('try_again.html') 


###############################
@app.route('/show_menu', methods=['GET'])       #on submission of login details
def show_menu(): 
   return render_template('show_menu.html')

############### username ##########
def return_user():
   username = user
   return username


######################## Profile ##############################
@app.route('/profile/')
def profile():
   sql = "SELECT * FROM user \
          WHERE username = '%s'" % (user)       #checking if user is already there in database
   try:  
      cursor.execute(sql)
      details = cursor.fetchall() 
   except:
      print "no user info"  
      
   return  render_template('profile.html',param=details)               #displaying the html

    
####################### default error handler ################    
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404
    
   
