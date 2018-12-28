from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

contingent_page = Blueprint('contingent_page', __name__, template_folder='templates', static_folder='static')   

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
############################# contingent functions ##################
@contingent_page.route('/')
def index():
	print "cont"
	return render_template('cont_index.html')


def createpdf(params):
	
	packet = StringIO.StringIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet,pagesize=A4)
	can.setFont("Helvetica", 10) 
	can.drawString(90, 520, params[0])
	can.drawString(150, 520, params[1])
	can.drawString(460, 520, params[2])
	can.drawString(90, 495, params[3])
	can.drawString(150, 495, params[4])
	can.drawString(460, 495, params[5])
	can.drawString(90, 470, params[6])
	can.drawString(150, 470, params[7])
	can.drawString(460, 470, params[8])
	can.drawString(90, 445, params[9])
	can.drawString(150, 445, params[10])
	can.drawString(460, 445, params[11])
	can.drawString(460, 398, params[12])
	can.drawString(90, 260, params[13])
	can.drawString(130, 245, params[14])
	can.drawString(425, 215, params[15])
	can.drawString(425, 197, params[16])
	can.drawString(230, 85, params[17])
	can.drawString(230, 63, params[18])
	can.drawString(230, 40, params[19])
	can.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	# read your existing PDF
	pdfname = "contingent/static/CONTINGENT_EXPENDITURE.pdf"
	print pdfname
	existing_pdf = PdfFileReader(file(pdfname, "rb"))
	output = PdfFileWriter()

	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)

	cur.execute("SELECT max(formnum) FROM contingent_forms")
	count = cur.fetchall()
	print count[0][0]

	# finally, write "output" to a real file
	outpdfname = "contingent/static/downloads/" + str(count[0][0]) + ".pdf"
	outputStream = file(outpdfname, "wb")
	output.write(outputStream)
	outputStream.close()
	return


@contingent_page.route('/insert', methods =['GET', 'POST'])
def insert():
	if (request.method =='POST'):
		dt1=request.form['dt1']
		des1=request.form['des1']
		amt1=request.form['amt1']
		dt2=request.form['dt2']
		des2=request.form['des2']
		amt2=request.form['amt2']
		dt3=request.form['dt3']
		des3=request.form['des3']
		amt3=request.form['amt3']
		dt4=request.form['dt4']
		des4=request.form['des4']
		amt4=request.form['amt4']
		Total=request.form['total']
		curr_date=request.form['curr_date']
		Station=request.form['station']
		Name=request.form['name']
		Address=request.form['address']
		BankBranch=request.form['bankbranch']
		AcNum=request.form['acNum']
		IFSC=request.form['ifsc']
		
		print dt1,des1,amt1,dt2, des2,amt2,dt3,des3,amt3,dt4,des4,amt4,Total,curr_date,\
					Station,Name,Address,BankBranch,AcNum,IFSC
		
		sql = "INSERT INTO contingent_forms (dt1,des1,amt1,dt2,des2,amt2,dt3,des3,amt3,dt4,des4,amt4,\
				total,curr_date,station,name,address,bankbranch,acnum,ifsc) values('%s','%s','%d','%s',\
				'%s','%d','%s','%s','%d','%s','%s','%d','%d','%s','%s','%s','%s','%s','%s','%s')" \
				% (dt1,des1,int(amt1),dt2, des2,int(amt2),dt3,des3,int(amt3),dt4,des4,int(amt4),int(Total)\
					,curr_date,Station,Name,Address,BankBranch,AcNum,IFSC)

		try:   
		   cur.execute(sql)
		   conn.commit()
		   params = [dt1,des1,amt1,dt2,des2,amt2,dt3,des3,amt3,dt4,des4,amt4,Total,Station,curr_date,\
					Name,Address,BankBranch,AcNum,IFSC]
		   createpdf(params)
		   msg="Form is stored"
		   return render_template('cont_message.html',msg = msg)
		except:
		   return render_template('cont_message.html',msg = "Error!! Try again")
	return "Database connection error"

# @contingent_page.route('/update')
# def update():
# 	cur.execute("SELECT formnum,curr_date,name,total FROM contingent_forms")
# 	rows = cur.fetchall()
# 	return render_template("cont_update.html", rows = rows)


# @contingent_page.route('/testupdate', methods =['GET', 'POST'])
# def testupdate():
# 	formnum = request.form['formnum']
# 	dt1=request.form['dt1']
# 	des1=request.form['des1']
# 	amt1=request.form['amt1']
# 	dt2=request.form['dt2']
# 	des2=request.form['des2']
# 	amt2=request.form['amt2']
# 	dt3=request.form['dt3']
# 	des3=request.form['des3']
# 	amt3=request.form['amt3']
# 	dt4=request.form['dt4']
# 	des4=request.form['des4']
# 	amt4=request.form['amt4']
# 	Total=request.form['total']
# 	curr_date=request.form['curr_date']
# 	Station=request.form['station']
# 	Name=request.form['name']
# 	Address=request.form['address']
# 	BankBranch=request.form['bankbranch']
# 	AcNum=request.form['acNum']
# 	IFSC=request.form['ifsc']
# 	sql = "UPDATE contingent_forms set name='%s', designation='%s', department='%s', id='%s',bill='%d', date='%s',\
# 		 bank='%s', account='%d', ifsc='%s' where formnum ='%d' " %(name, designation, department, id, int(bill), \
# 		 date, bank, int(account), ifsc, int(formnum))
# 	cur.execute(sql)
# 	conn.commit()
# 	return render_template('cont_message.html', msg = "Form has been Updated")


@contingent_page.route('/delete')
def delete():
	cur.execute("SELECT formnum,name,curr_date,total FROM contingent_forms")
	rows =cur.fetchall()
	return render_template("cont_delete.html", rows =rows)


@contingent_page.route('/testdelete', methods =['GET', 'POST'])
def testdelete():
	formnum = int(request.form['formnum'])
	sql = "DELETE FROM contingent_forms WHERE formnum='%d' " %(formnum)
	cur.execute(sql)
	conn.commit()
	return render_template('cont_message.html', msg = "Form is Deleted")
		

@contingent_page.route('/display')
def display():
	cur.execute("SELECT formnum,name,curr_date,total FROM contingent_forms")
	rows = cur.fetchall()
	return render_template('cont_display.html',rows = rows)
