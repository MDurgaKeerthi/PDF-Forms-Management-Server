from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

sdb_page = Blueprint('sdb_page', __name__, template_folder='templates')   

########################### database connection ################
#!/usr/bin/python
import mysql.connector as mariadb
conn = mariadb.connect(user='root', password='123', database='cc_manager')
  #username for database, password, databasename
cur = conn.cursor()

######################### sdb functions ##################

@sdb_page.route('/')
def index():
	return render_template('index.html')


