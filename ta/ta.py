from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

ta_page = Blueprint('ta_page', __name__, template_folder='templates',static_folder='static')   

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
############################# ta functions ##################
@ta_page.route('/')
def index():
	return render_template('ta_index.html')


def createpdf(name,srn,dsgn,dpt,inst,bp,ipac,poj,ds,dd,dtym,arst,ad,atym,moj,jc,\
		   			road,tktno,fare,amt11,sn,exp,bill,amt22,amt33,enc,date,amt44,amt55,AB,\
		   			advdrawn,netclaimed,excesspaid,excessrecovered,bankname,ifsc,accno):
	
	print "hiii"
	print name,srn,dsgn,dpt,inst,bp,ipac,poj,ds,dd,dtym,arst,ad,atym,moj,jc,\
		   			road,tktno,fare,amt11,sn,exp,bill,amt22,amt33,enc,date,amt44,amt55,AB,\
		   			advdrawn,netclaimed,excesspaid,excessrecovered,bankname,ifsc,accno
	packet = StringIO.StringIO()
	# create a new PDF with Reportlab
	can = canvas.Canvas(packet,pagesize=A4)
	can.setFont("Helvetica", 10) 
	can.drawString(95, 692, name)
	can.drawString(355,692, srn)
	can.drawString(113,673, dsgn)
	can.drawString(240,673, dpt)
	can.drawString(345,673, inst)
	can.drawString(113,653, bp)
	can.drawString(494,651, ipac)
	can.drawString(140,632, poj)
	can.drawString(78,550, ds)
	can.drawString(122,550,dd)
	can.drawString(175,550, dtym)
	can.drawString(215,550, arst)
	can.drawString(275,550, ad)
	can.drawString(326,550, atym)
	can.drawString(360, 550, moj)
	can.drawString(405,550, jc)
	can.drawString(442,550, road)
	can.drawString(478,550, tktno)
	can.drawString(560,550, fare)
	# can.drawString(78,525, "dstn")
	# can.drawString(122,525,"ddate")
	# can.drawString(175,525, "dtime")
	# can.drawString(215,525, "astn")
	# can.drawString(275,525, "adt")
	# can.drawString(326,525, "atime")
	# can.drawString(360, 525, "modeofjourney")
	# can.drawString(405,525, "class")
	# can.drawString(442,525, "road")
	# can.drawString(478,525, "tktno")
	# can.drawString(560,525, "fare")
	can.drawString(550,390, amt11)
	can.drawString(52,330, sn)
	can.drawString(90,330, exp)
	can.drawString(460,330, amt22)
	can.drawString(525,330, bill)
	can.drawString(525,252.5, amt33)
	can.drawString(130,241, enc)
	can.drawString(80,231.5, date)
	can.drawString(280,223, amt44)
	can.drawString(362,223, amt55)
	can.drawString(215,204, AB)
	can.drawString(215,194, advdrawn)
	can.drawString(215,184, netclaimed)
	can.drawString(215,174, excesspaid)
	can.drawString(215,165, excessrecovered)
	can.save()

	#move to the beginning of the StringIO buffer
	packet.seek(0)
	new_pdf = PdfFileReader(packet)

	# read your existing PDF
	pdfname = "ta/static/TA.pdf"
	print pdfname
	existing_pdf = PdfFileReader(file(pdfname, "rb"))
	output = PdfFileWriter()

	# add the "watermark" (which is the new pdf) on the existing page
	page = existing_pdf.getPage(0)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)

	packet1 = StringIO.StringIO()
	can1 = canvas.Canvas(packet1,pagesize=A4)
	can1.setFont("Helvetica", 10) 
	can1.drawString(230, 506.5, bankname)
	can1.drawString(230, 495, accno)
	can1.drawString(230, 485, ifsc)
	can1.save()
	packet1.seek(0)
	new_pdf = PdfFileReader(packet1)	
	page = existing_pdf.getPage(1)
	page.mergePage(new_pdf.getPage(0))
	output.addPage(page)

	cur.execute("SELECT max(formnum) FROM ta_forms")
	count = cur.fetchall()
	print count[0][0]

	# finally, write "output" to a real file
	outpdfname = "ta/static/downloads/" + str(count[0][0]) + ".pdf"
	outputStream = file(outpdfname, "wb")
	output.write(outputStream)
	outputStream.close()
	return


@ta_page.route('/insert', methods =['GET', 'POST'])
def insert():
	if (request.method =='POST'):
		name=request.form['name']
		srn=request.form['s_rno']
		dsgn=request.form['designation']
		dpt=request.form['department']
		inst=request.form['institute']
		bp =request.form['basic_pay']
		ipac=request.form['inst_prjacno']
		poj=request.form['purposeofjourney']
		ds=request.form['dstn']
		dd=request.form['ddate']
		dtym=request.form['dtime']
		arst=request.form['astn']
		ad=request.form['adt']
		atym=request.form['atime']
		moj=request.form['modeofjourney']
		jc=request.form['class']
		road=request.form['road']
		tktno=request.form['tktno']
		fare=request.form['fare']
		amt11=request.form['total_claimed1']
		sn=request.form['sno']
		exp=request.form['expenditure']
		bill=request.form['bill_details']
		amt22=request.form['amt']
		amt33=request.form['total_claimed2']
		enc=request.form['enclosures']
		date=request.form['pdate']
		amt44=request.form['amt2']
		amt55=request.form['amt3']
		AB=request.form['a_b']
		advdrawn=request.form['adv_drawn']
		netclaimed=request.form['net_claim']
		excesspaid=request.form['paid_excess']
		excessrecovered=request.form['recovered_excess']
		bankname=request.form['bname_branch']
		ifsc=request.form['ifsc']
		accno=request.form['acno']
		

		sql = "INSERT INTO ta_forms (name,s_rno,designation,department,institute,basic_pay,\
				inst_prjacno,purposeofjourney,dstn,ddate,dtime,astn,adt,atime,modeofjourney,\
				class,road,tktno,fare,total_claimed1,sno,expenditure,bill_details,amt,\
				total_claimed2,enclosures,pdate,amt2,amt3,a_b,adv_drawn,net_claim,\
				paid_excess,recovered_excess,bname_branch,ifsc,acno) \
				VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
				'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',\
				'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format (name,\
					srn,dsgn,dpt,inst,bp,ipac,poj,ds,dd,dtym,arst,ad,atym,moj,jc,road,tktno,fare,\
					amt11,sn,exp,bill,amt22,amt33,enc,date,amt44,amt55,AB,advdrawn,netclaimed,\
					excesspaid,excessrecovered,bankname,ifsc,accno)
		try:   
		   cur.execute(sql)
		   conn.commit()
		   createpdf(name,srn,dsgn,dpt,inst,bp,ipac,poj,ds,dd,dtym,arst,ad,atym,moj,jc,\
		   			road,tktno,fare,amt11,sn,exp,bill,amt22,amt33,enc,date,amt44,amt55,AB,\
		   			advdrawn,netclaimed,excesspaid,excessrecovered,bankname,ifsc,accno)
		   msg="Form is stored"
		   return render_template('ta_message.html',msg = msg)
		except:
		   return render_template('ta_message.html',msg = "Error!! Try again")
	return "Database connection error"


# @ta_page.route('/update')
# def update():
# 	cur.execute("SELECT * FROM ta_forms")
# 	rows = cur.fetchall()
# 	return render_template("ta_update.html", rows = rows)


# @ta_page.route('/testupdate', methods =['GET', 'POST'])
# def testupdate():
# 	formnum = request.form['formnum']
# 	name=request.form['name']
# 	srn=request.form['s_rno']
	
# 	dsgn=request.form['designation']
# 	dpt=request.form['department']
	
# 	inst=request.form['institute']
# 	bp =request.form['basic_pay']
	
# 	ipac=request.form['inst_prjacno']
# 	poj=request.form['purposeofjourney']
	
# 	ds=request.form['dstn']
# 	dd=request.form['ddt']
# 	dtym=request.form['dtime']
# 	arst=request.form['astn']
# 	ad=request.form['adt']
# 	atym=request.form['atime']
# 	moj=request.form['modeofjourney']
# 	jc=request.form['class']
# 	road=request.form['road']
# 	tktno=request.form['tktno']
# 	fare=request.form['fare']
	
# 	amt1_=request.form['total_claimed1']
	
# 	sn=request.form['sno']
# 	exp=request.form['expenditure']
# 	bill=request.form['bill_details']
# 	amt2_=request.form['amt']
	
# 	amt3_=request.form['total_claimed2']
	
# 	enc=request.form['enclosures']
# 	date=request.form['pdate']
# 	amt4_=request.form['amt2']
# 	amt5_=request.form['amt3']
# 	advdrawn=request.form['adv_drawn']
# 	netclaimed=request.form['net_claim']
# 	excesspaid=request.form['paid_excess']
# 	excessrecovered=request.form['recovered_excess']
	
# 	bankname=request.form['bname_branch']
# 	ifsc=request.form['ifsc']
# 	accno=request.form['acno']
# 	sql = "UPDATE ta_forms set name='%s', designation='%s', department='%s', id='%s',bill='%d', date='%s',\
# 		 bank='%s', account='%d', ifsc='%s' where formnum ='%d' " %(name, designation, department, id, int(bill), \
# 		 date, bank, int(account), ifsc, int(formnum))
# 	cur.execute(sql)
# 	conn.commit()
# 	return render_template('ta_message.html', msg = "Form has been Updated")


@ta_page.route('/delete')
def delete():
	cur.execute("SELECT formnum,s_rno,pdate,purposeofjourney,net_claim FROM ta_forms")
	rows =cur.fetchall()
	return render_template("ta_delete.html", rows =rows)


@ta_page.route('/testdelete', methods =['GET', 'POST'])
def testdelete():
	formnum = int(request.form['formnum'])
	sql = "DELETE FROM ta_forms WHERE formnum='%d' " %(formnum)
	cur.execute(sql)
	conn.commit()
	return render_template('ta_message.html', msg = "Form is Deleted")
		

@ta_page.route('/display')
def display():
	cur.execute("SELECT formnum,s_rno,pdate,purposeofjourney,net_claim FROM ta_forms")
	rows = cur.fetchall()
	return render_template('ta_display.html',rows = rows)
