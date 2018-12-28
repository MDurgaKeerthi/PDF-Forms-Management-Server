from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

travel_page = Blueprint('travel_page', __name__, template_folder='templates',static_folder='static')   

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
############################# travel functions ##################
@travel_page.route('/')
def index():
	print "travel"
	return render_template('travel_index.html')


def createpdf(name,desigtn,dept,basic_p,d_o_j1,d_o_j2,p_o_j,s_no,c_o_j,e_o_f,acc_chrg,\
		   			exp,details,ad_req,ta_no,ta_ad,rup,b_name, b_acc,ifs):
	print "here"

	packet = StringIO.StringIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet,pagesize=A4)
	can.setFont("Helvetica", 10) 
	can.drawString(250, 602, name)
	can.drawString(505, 598, s_no)
	can.drawString(250, 584, desigtn)
	can.drawString(250, 568, dept)
	can.drawString(250,551, basic_p)
	can.drawString(240,532, d_o_j1)
	can.drawString(292,532, d_o_j2)
	can.drawString(230,514, p_o_j)
	can.drawString(290,442, c_o_j)
	can.drawString(350,442, e_o_f)
	# can.drawString(442,442, "3326")
	can.drawString(350,420, acc_chrg)
	# can.drawString(442,420, "3326")
	can.drawString(350,398, exp)
	# can.drawString(442,398, "3326")
	can.drawString(150,380, details)
	can.drawString(335,353, ad_req)
	can.drawString(130,203, ta_no)
	can.drawString(225,160, ta_ad)
	can.drawString(130,143, rup)
	can.drawString(225,58, b_name)
	can.drawString(225,47, b_acc)
	can.drawString(225,37, ifs)
	can.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	# read your existing PDF
	pdfname = "travel/static/TRAVEL_ADVANCE_FORM_final.pdf"
	print pdfname
	existing_pdf = PdfFileReader(file(pdfname, "rb"))
	output = PdfFileWriter()

	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)

	cur.execute("SELECT max(formnum) FROM travel_forms")
	count = cur.fetchall()
	print count[0][0]

	# finally, write "output" to a real file
	outpdfname = "travel/static/downloads/" + str(count[0][0]) + ".pdf"
	outputStream = file(outpdfname, "wb")
	output.write(outputStream)
	outputStream.close()
	return


@travel_page.route('/insert', methods =['GET', 'POST'])
def insert():
	if (request.method =='POST'):
		name=request.form['name']
		desigtn=request.form['desigtn']
		dept=request.form['dept']
		basic_p=request.form['basic_p']
		d_o_j1=request.form['d_o_j1']
		d_o_j2=request.form['d_o_j2']
		p_o_j=request.form['p_o_j']
		s_no=request.form['s_no']
		c_o_j=request.form['c_o_j']
		e_o_f=request.form['e_o_f']
		acc_chrg=request.form['acc_chrg']
		exp=request.form['exp']
		details=request.form['details']
		ad_req=request.form['ad_req']
		ta_no=request.form['ta_no']
		ta_ad=request.form['ta_ad']
		rup=request.form['rup']
		b_name=request.form['b_name']
		b_acc=request.form['b_acc']
		ifsc=request.form['ifsc']
		
		sql = "INSERT INTO travel_forms (name,desigtn,dept,basic_p,d_o_j1,d_o_j2,p_o_j,\
				s_no,c_o_j,e_o_f,acc_chrg,exp,details,ad_req,ta_no,ta_ad,rup,b_name,b_acc,ifsc)\
				values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
				'{}','{}','{}','{}','{}','{}')".format(name,desigtn,dept,basic_p,d_o_j1,d_o_j2,\
					p_o_j,s_no,c_o_j,e_o_f,acc_chrg,exp,details,ad_req,ta_no,ta_ad,rup,b_name,\
					b_acc,ifsc)
		try:   
		   cur.execute(sql)
		   conn.commit()
		   createpdf(name,desigtn,dept,basic_p,d_o_j1,d_o_j2,p_o_j,s_no,c_o_j,e_o_f,acc_chrg,\
		   			exp,details,ad_req,ta_no,ta_ad,rup,b_name, b_acc,ifsc)
		   msg="Form is stored"
		   return render_template('travel_message.html',msg = msg)
		except:
		   return render_template('travel_message.html',msg = "Error!! Try again")
	return "Database connection error"

# @travel_page.route('/update')
# def update():
# 	cur.execute("SELECT * FROM travel_forms")
# 	rows = cur.fetchall()
# 	return render_template("travel_update.html", rows = rows)


# @travel_page.route('/testupdate', methods =['GET', 'POST'])
# def testupdate():
# 	formnum = request.form['formnum']
# 	name = request.form['name']
# 	designation = request.form['designation']
# 	department = request.form['department']
# 	id = request.form['id']
# 	bill = request.form['bill']
# 	date = request.form['date']
# 	bank = request.form['bank']
# 	account = request.form['account']
# 	ifsc = request.form['ifsc']
# 	sql = "UPDATE travel_forms set name='%s', designation='%s', department='%s', id='%s',bill='%d', date='%s',\
# 		 bank='%s', account='%d', ifsc='%s' where formnum ='%d' " %(name, designation, department, id, int(bill), \
# 		 date, bank, int(account), ifsc, int(formnum))
# 	cur.execute(sql)
# 	conn.commit()
# 	return render_template('travel_message.html', msg = "Form has been Updated")


@travel_page.route('/delete')
def delete():
	cur.execute("SELECT formnum,s_no,d_o_j1,p_o_j, ad_req FROM travel_forms")
	rows =cur.fetchall()
	return render_template("travel_delete.html", rows =rows)


@travel_page.route('/testdelete', methods =['GET', 'POST'])
def testdelete():
	formnum = int(request.form['formnum'])
	sql = "DELETE FROM travel_forms WHERE formnum='%d' " %(formnum)
	cur.execute(sql)
	conn.commit()
	return render_template('travel_message.html', msg = "Form is Deleted")
		

@travel_page.route('/display')
def display():
	cur.execute("SELECT formnum,s_no,d_o_j1,p_o_j, ad_req  FROM travel_forms")
	rows = cur.fetchall()
	return render_template('travel_display.html',rows = rows)
