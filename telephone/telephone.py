from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

telephone_page = Blueprint('telephone_page', __name__, template_folder='templates',static_folder='static')   

########################### database connection ################
#!/usr/bin/python
import mysql.connector as mariadb
conn = mariadb.connect(user='root', password='123', database='cc_manager')
  #username for database, password, databasename
cur = conn.cursor()

####################################################################
from pyPdf import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
############################# telephone functions ##################
@telephone_page.route('/')
def index():
	print "tele"
	return render_template('tele_index.html')

def getmonth(mo):	
	# print mo, type(mo)
	if mo == "01":
		return "January"
	elif mo == "02":
		return "February"
	elif mo == "03":
		return "March"
	elif mo == "04":
		return "April"
	elif mo == "05":
		return "May"
	elif mo == "06":
		return "June"
	elif mo == "07":
		return "July"
	elif mo == "08":
		return "August"
	elif mo == "09":
		return "Septemeber"
	elif mo == "10":
		return "October"
	elif mo == "11":
		return "November"
	elif mo == "12":
		return "December"
	elif mo == "00":
		return "."

def createpdf(name,designation,department,id,bill,date,bank,account,ifsc):
	print "here"
	if name == "":
		name = "."
	if designation == "":
		designation = "."
	if department == "":
		department = "."
	if id == "":
		id = "."
	if date == "":
		date = "1111/00/11"
	if bank == "":
		bank = "."
	if account == "":
		account = "."
	if ifsc == "":
		ifsc = "."




	packet = StringIO.StringIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet,pagesize=A4)
	can.setFont("Helvetica", 10) 
	can.drawString(505, 593, date)
	can.drawString(397, 480, bill)
	month = getmonth(str(date[5])+str(date[6]))
	can.drawString(300, 463, month)
	can.drawString(240, 445, month)
	can.drawString(482, 372, name)
	can.drawString(482, 358, designation)
	can.drawString(482, 345, department)
	can.drawString(482, 333, id)	
	can.drawString(230, 296.5, bank)
	can.drawString(230, 275, account)
	can.drawString(230, 252, ifsc)
	can.save()

	print name,designation,department,id,bill,date,bank,account,ifsc,month
	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	# read your existing PDF
	pdfname = "telephone/static/Telephone_Reimbursement.pdf"
	print pdfname
	existing_pdf = PdfFileReader(file(pdfname, "rb"))
	output = PdfFileWriter()

	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)

	cur.execute("SELECT max(formnum) FROM telephone_forms")
	count = cur.fetchall()
	print count[0][0]

	# finally, write "output" to a real file
	outpdfname = "telephone/static/downloads/" + str(count[0][0]) + ".pdf"
	outputStream = file(outpdfname, "wb")
	output.write(outputStream)
	outputStream.close()
	return


@telephone_page.route('/insert', methods =['GET', 'POST'])
def insert():
	if (request.method =='POST'):
		name = request.form['name']
		designation = request.form['designation']
		department = request.form['department']
		id = request.form['id']
		bill = request.form['bill']
		date = request.form['date']
		bank = request.form['bank']
		account = request.form['account']
		ifsc = request.form['ifsc']
		
		sql = "INSERT INTO telephone_forms (name, designation, department, id, bill, date, bank, account, ifsc) \
				VALUES('%s','%s','%s','%s','%d','%s','%s','%s','%s') " \
				% (name, designation, department, id, int(bill), date, bank,account, ifsc)
		try:   
		   cur.execute(sql)
		   conn.commit()
		   print name, designation,department,id,bill,date,bank,account,ifsc, "deahsdbsk"
		   createpdf(name, designation,department,id,bill,date,bank,account,ifsc)
		   msg="Form is stored"
		   return render_template('tele_message.html',msg = msg)
		except:
		   return render_template('tele_message.html',msg = "Error!! Try again")
	return "Database connection error"

@telephone_page.route('/update')
def update():
	cur.execute("SELECT * FROM telephone_forms")
	rows = cur.fetchall()
	return render_template("tele_update.html", rows = rows)


@telephone_page.route('/testupdate', methods =['GET', 'POST'])
def testupdate():
	formnum = request.form['formnum']
	name = request.form['name']
	designation = request.form['designation']
	department = request.form['department']
	id = request.form['id']
	bill = request.form['bill']
	date = request.form['date']
	bank = request.form['bank']
	account = request.form['account']
	ifsc = request.form['ifsc']
	sql = "UPDATE telephone_forms set name='%s', designation='%s', department='%s', id='%s',bill='%d', date='%s',\
		 bank='%s', account='%s', ifsc='%s' where formnum ='%d' " %(name, designation, department, id, int(bill), \
		 date, bank, account, ifsc, int(formnum))
	cur.execute(sql)
	conn.commit()
	return render_template('tele_message.html', msg = "Form has been Updated")


@telephone_page.route('/delete')
def delete():
	cur.execute("SELECT * FROM telephone_forms")
	rows =cur.fetchall()
	return render_template("tele_delete.html", rows =rows)


@telephone_page.route('/testdelete', methods =['GET', 'POST'])
def testdelete():
	formnum = int(request.form['formnum'])
	sql = "DELETE FROM telephone_forms WHERE formnum='%d' " %(formnum)
	cur.execute(sql)
	conn.commit()
	return render_template('tele_message.html', msg = "Form is Deleted")
		

@telephone_page.route('/display')
def display():
	cur.execute("SELECT * FROM telephone_forms")
	rows = cur.fetchall()
	return render_template('tele_display.html',rows = rows)
