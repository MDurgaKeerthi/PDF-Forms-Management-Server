import os
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

from server import app
#################### connect to database ###############
#!/usr/bin/python
import mysql.connector as mariadb
db = mariadb.connect(user='root', password='123', database='cc_manager')
  #username for database, password, databasename
cursor = db.cursor()

###############################################################

def isnum(num):
   if num == "1" :
      return 1
   if num == "2" :
      return 2
   if num == "3" :
      return 3
   if num == "4" :
      return 4
   if num == "5" :
      return 5
   if num == "6" :
      return 6
   if num == "7" :
      return 7
   if num == "8" :
      return 8
   if num == "9" :
      return 9   
   if num == "0" :
      return 0
   else :
      return 11      
      
def extractnum(line, index):
   print line
   while isnum(line[index]) == 11:
      print line[index], index
      index += 1
   num = 0.0
   num1 = 0.0
   flag = -1
   while line[index] != " ":
      if line[index] == ".":
         flag = 0
         num = num*1.0 + isnum(line[index+1])*0.1 + isnum(line[index+2])*0.01
         index += 3
         break
      if isnum(line[index]) != 11 and flag != 0:
         num = num*10.0 + isnum(line[index])
      index += 1  
      
   if flag == 0 and line[index]==" ":      
      print num, line[index],"csdf" 
      return num
   else: 
      return -1   
   
def extractString(line, start):
   i=start+1
   
   l = len(line)
   str1 = ""
   num = -1
   while num == -1:
      while isnum(line[i]) == 11 and i< (l-1):
         i = i+1
      
      i1 = i
      i = i-1
      while line[i] == " " and i>=0:
         i = i-1
      
      num = extractnum(line,i1)
      
      if num == -1:
         i = i1
         while line[i] != " " and (line[i] == "," or isnum(line[i]) != 11) :
            i = i+1
      
   j=start+1
   while j<=i:
      str1 = str1 + line[j]
      j = j+1 

   return str1, num


def extractpdf(pdfname, ccsid):
   str1 = "pdftotext -layout "+ os.path.join(app.config['UPLOAD_FOLDER'], pdfname)
   print str1
   os.system(str1)

   name = os.path.join(app.config['UPLOAD_FOLDER']) + pdfname[:-3] + "txt"
   readfrom = open(name, "r+")

   flag = 0
   line = 0
   for text in readfrom :
    lineindex = 0
    if "NEFT" in text :
      flag = 1
      line = 0
    if flag == 2:
      break  
    if flag == 1 and line != 3:  
      while(isnum(text[lineindex]) ==11):
         if line == 2:
            break
         lineindex += 1 
         if lineindex == len(text):  
            flag = 2
            break 
         #if isnum(text[0]) == 11:        #loops till the end of the table
         #   break
      if flag != 2 :
         j=0
         date = ""
         while j < 9 :
            date = date + text[lineindex]
            lineindex += 1
            j = j+1
         
         trd, amt = extractString(text,lineindex)

         sql = "INSERT INTO transactions(date, ccs_no, transactional_details, amount, header, files_uploaded) \
                        VALUES ('%s', '%d', '%s', '%f', '%s', '%d')" % \
                        (date, ccsid, trd, amt, 'IITH', 0)       #registering the visitor
         try:
                  print "inserted" 
                  cursor.execute(sql)
                  db.commit()
         except:
                  print "Error: unable to insert data" 
                  db.rollback()  
    line+=1
   
   
   pagenum = 1
   while 1: 
      proceed = 0
      pagenum += 1     

      flag = 0
      line = 0
      for text in readfrom :
       lineindex = 0
       if "Transaction Details" in text :
         proceed = 1
         line = 0
       if flag == 2:
         break  
       if  proceed == 1 and line >= 4:
         while(isnum(text[lineindex]) == 11):
            lineindex += 1 
            if lineindex == len(text):  
               flag = 2
               break 
            #if isnum(text[0]) == 11:        #loops till the end of the table
            #   break
         if flag != 2:
            j=0
            date = ""
            while j < 9 :
               date = date + text[lineindex]
               lineindex += 1
               j = j+1
            
            trd, amt = extractString(text,lineindex)

            sql = "INSERT INTO transactions(date, ccs_no, transactional_details, amount, header, files_uploaded) \
                           VALUES ('%s', '%d', '%s', '%f', '%s', '%d')" % \
                           (date, ccsid, trd, amt, 'IITH', 0)       #registering the visitor
            try:
                     print "inserted" 
                     cursor.execute(sql)
                     db.commit()
            except:
                     print "Error: unable to insert data" 
                     db.rollback()  
       line += 1  
      if proceed == 0:
       break
   readfrom.close()    
   os.remove(name)   

##########################################################################   

user = ""
total = []
res = ()
no_css = 0

def getparam():
   global total, res
   sql = "SELECT * FROM cc_statement"      #getting all the data
   try:
      cursor.execute(sql)
      res = cursor.fetchall()
      total = []
      no_css = len(res)
      print no_css,res[0][3],"...\n"
      for i in range(no_css):
         print 'in loop'
         sql = "SELECT * FROM transactions\
                        WHERE ccs_no = '%d'" % (res[i][0])
         try:
            cursor.execute(sql)
            alltrans = cursor.fetchall()
            total.append(alltrans) 
         except:
            print "Error: unable to fetch trans data"  
   except:
      print "Error: unable to fetch data from getparam()"          
   return 
   
############################################################

ccsm_page = Blueprint('ccsm_page', __name__, template_folder='templates', static_folder='static')   
        
##############-----starts here-----------###################
def setuser():
   from server import return_user
   global user
   user = return_user()
   
@ccsm_page.route('/')
def start_ccsm():
   print user, "got it"
   getparam()
   return render_template('actions.html', param=total, ccsnames = res)    
    
    
##############-----uploading file-----------###################    
app.config['UPLOAD_FOLDER'] = 'ccsm/static/uploads/'
app.config['UPLOAD_BILLS'] = 'ccsm/static/bills/'
app.config['ALLOWED_EXTENSIONS'] = set(['pdf', 'txt'])
#pdfstatements = Flask.UploadSet('pdfstatements', PDFS)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@ccsm_page.route('/upload', methods=['POST'])      #upload file webpage
def upload():
    if request.method == 'GET':
       getparam() 
       return render_template('actions.html',param=total, ccsnames = res)       #get request
    else :  
       filetype = request.form['filetype']
       today = request.form['today']
       date = str(today[-2:] + today[4:8] + today[:4])
       
       if filetype == "ccs":
          file = request.files['file']                #on submission of file to be uploaded
          if file and allowed_file(file.filename):
              filename = secure_filename(file.filename)  #checking if the file is valid            

              ccsid = 0  
              sql = "SELECT * FROM cc_statement"      
              try:  
                  cursor.execute(sql)
                  results1 = cursor.fetchall()
                  ccsid = len(results1) + 1
              except:
                  print "try other"

              filen = 'ccs' + str(ccsid) + '-' + user + ".pdf"  #rename file
              
              sql = "INSERT INTO cc_statement(ccsname, uploaded_date, uploader, no_of_bills) \
                     VALUES ('%s', '%s', '%s','%d')" % \
                     (filen, date, user, 0)       #registering the visitor
              try:
               
               cursor.execute(sql)
               db.commit()
               print "yep ccs"
              except:
               print "Error: unable to insert data" 
               db.rollback()

              file.save(os.path.join(app.config['UPLOAD_FOLDER'], filen))    
   
              extractpdf(filen,ccsid)       
              return redirect(url_for('ccsm_page.start_ccsm'))
       elif filetype == "bill":
           files = request.files.getlist("file[]")
           transid = request.form.getlist("transid")
           ccs_no = int(request.form['ccs_no'])
           print ccs_no
           ccs = ""
           sql = "SELECT * FROM cc_statement \
                        WHERE ccsid = '%d'" % (ccs_no)     #getting the images uploaded by user
           try:
               cursor.execute(sql)
               records = cursor.fetchall()
               ccs = records[0][1]
           except:
               print "Error: Unable to fetch ccs name" 
               
           index = -1
           billsno = 0  
           billid = []     
           print transid
           for file in files:   
              if file and allowed_file(file.filename):
                 filename = secure_filename(file.filename)  
		 index = index + 1 
                 num = int(transid[index])
                 print num,"  is \n"
                 billsno += 1
                 
                 sql = "SELECT * FROM bills"
                 cursor.execute(sql)
                 temp_res = cursor.fetchall()
                 billnum = len(temp_res) + 1
                 billid.append(billnum)
                 filen = 'bill' + str(billid[billsno-1]) + '-' + user + filename[-4:]  #rename file
                 sql = "INSERT INTO bills(billname, ccsname, transactionid, uploader, date) \
                           VALUES ('%s', '%s', '%d', '%s', '%s')" % \
                           (filen, ccs, num, user, date)   
                 try:
                     cursor.execute(sql)
                     db.commit()
                     print "inserted into bills"
                 except:
                     db.rollback()
                 
                 file.save(os.path.join(app.config['UPLOAD_BILLS'], filen))  #saving the file to uploads folder
              
                 sql = "UPDATE transactions SET files_uploaded = files_uploaded + 1 WHERE transactionid = '%d'" % (num)
                 try:
                        cursor.execute(sql)
                        db.commit()
                        print "updated files_uploaded"
                 except:
                        db.rollback()
           print billsno, ccs_no              
           if billsno > 0:
               sql = "UPDATE cc_statement SET no_of_bills = no_of_bills + '%d' WHERE ccsid = '%d'" % (billsno,ccs_no)
               try:
                        cursor.execute(sql)
                        db.commit()
                        print "updated files_uploaded"
               except:
                        db.rollback()
               getparam()                    
               return render_template('alert_actions.html',fileid = billnum,param=total, ccsnames = res)  
    return render_template('ccsm_message.html',msg="error")

#############################################################

@ccsm_page.route('/downloads')    
def downloads():   
   getparam()
   sql = "SELECT * FROM bills \
                        ORDER BY ccsname, transactionid ASC"     #getting the images uploaded by user
   try:
      cursor.execute(sql)
      param2 = cursor.fetchall()
   except:
      print "Error: Unable to fetch ccs name" 
   return render_template('downloads.html', param1=res, param2 = param2)

##############################################################

import xlsxwriter
from PyPDF2 import PdfFileMerger
merger = PdfFileMerger(strict=False)

@ccsm_page.route('/mixpdf',methods=['POST'])       #on submission of login details
def mixpdf():
    pdfidlist = request.form.getlist("pdfid")
    pdflist = request.form.getlist("pdfname")
    for num in pdfidlist:
        thispdf = "ccsm/static/bills/" + str(pdflist[int(num)-1])
        merger.append(thispdf)
        print thispdf, type(thispdf)
    path, dirs, allfiles = next(os.walk("ccsm/static/downloads/"))
    file_name = str(len(allfiles))    
    merger.write("ccsm/static/downloads/do"+str(file_name)+".pdf")    
    return render_template('downloadfile.html', to_download="do"+str(file_name)+".pdf", ftype="pdf")    

@ccsm_page.route('/downloads/download_files',methods=['POST'])       #on submission of login details
def download_files():
   file_type = request.form['X']
   if file_type == "excel":
      file_name_id = int(request.form['fileid'])
      path, dirs, allfiles = next(os.walk("ccsm/static/downloads/"))
      file_name = str(len(allfiles))
      print file_name_id
      download_file = "ccsm/static/downloads/d_" + file_name + ".xlsx"   
      workbook = xlsxwriter.Workbook(download_file)
      worksheet = workbook.add_worksheet()
      row = 0
      col = 0
      worksheet.write('A1', 'Date')
      worksheet.write('B1', 'Transactional Details')
      worksheet.write('C1', 'Amount')
      worksheet.write('D1', 'Header')
      sql = "SELECT * FROM transactions \
                           WHERE ccs_no = '%d'" % (file_name_id)     
      try:
          cursor.execute(sql)
          records = cursor.fetchall()
          for record in records:
            print record
            row += 1   
            worksheet.write(row,0, record[1])  
            worksheet.write(row,1, record[3])  
            worksheet.write(row,2, record[4])
            worksheet.write(row,3, record[5])
          workbook.close()  
      except:
          print "Error: Unable to fetch records" 
   
      return render_template('downloadfile.html', to_download="d_" + file_name+ ".xlsx", ftype="excel")
   else:
      return render_template('error.html')
#######################################################

@ccsm_page.route('/history')    
def history():   
   allbills = ()
   sql = "SELECT * FROM bills ORDER BY transactionid ASC " 
   try:
            cursor.execute(sql)
            allbills = cursor.fetchall()
   except:
            print "Error: unable to fetch data"  
   
   getparam()
   return  render_template('history.html', param1=total, param2 = res, param3 = allbills)
   
###########----------Displaying the pics uploaded by the user------#########

