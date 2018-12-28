from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

rf_page = Blueprint('rf_page', __name__, template_folder='templates')   

########################### database connection ################
#!/usr/bin/python
import mysql.connector as mariadb
conn = mariadb.connect(user='root', password='123', database='cc_manager')
  #username for database, password, databasename
cur = conn.cursor()

############################# rf functions ##################
@rf_page.route('/')
def index():
	return render_template('index.html')


@rf_page.route('/act', methods =['GET', 'POST'])
def act():
	if (request.method =='POST'):
		s = request.form['serial']
		d = request.form['date']
		cash = request.form['cash']
		firm = request.form['firm']
		purpose = request.form['purpose']
		amount = request.form['amount']
		
		checksql = "select * from reimbursement_forms where serial = '%s' " % (s)
		cur.execute(checksql)
		res = cur.fetchall()
		if res == []:
		   sql = "INSERT INTO reimbursement_forms (serial, date,cash,firm,purpose,amount) VALUES('%s','%s','%d','%s','%s','%d') " % (s, d,int(cash),firm,purpose,int(amount))
		   cur.execute(sql)
		   conn.commit()
		   msg="Data Has Been Stored"
		   return render_template('message.html',msg =msg)
		else:
		   return render_template('message.html',msg = "serial number already exists! Please input correct data!!")
	return "Database connection error"

@rf_page.route('/update')
def update():
	cur.execute("SELECT * FROM reimbursement_forms")
	rows = cur.fetchall()
	return render_template("update.html", rows = rows)


@rf_page.route('/testupdate', methods =['GET', 'POST'])
def testupdate():
	s =request.form['serial']
	d =request.form['date']
	cash =request.form['cash']
	firm =request.form['firm']
	purpose =request.form['purpose']
	amount =request.form['amount']
	sql = "UPDATE reimbursement_forms set date='%s', cash='%d', firm ='%s', purpose='%s', amount='%d' where serial ='%s' " %(d,int(cash),firm,purpose,int(amount),s)
	cur.execute(sql)
	conn.commit()
	return render_template('message.html', msg = "Data has been Updated")


@rf_page.route('/delete')
def delete():
	cur.execute("SELECT * FROM reimbursement_forms")
	rows =cur.fetchall()
	return render_template("delete.html", rows =rows)


@rf_page.route('/testdelete', methods =['GET', 'POST'])
def testdelete():
	s =request.form['serial']
	sql = "DELETE FROM reimbursement_forms WHERE serial='%s' " %(s)
	cur.execute(sql)
	conn.commit()
	return render_template('message.html', msg = "Data has been Deleted")
		

@rf_page.route('/display')
def display():
	cur.execute("SELECT * FROM reimbursement_forms")
	rows = cur.fetchall()
	return render_template('display.html',rows = rows)



