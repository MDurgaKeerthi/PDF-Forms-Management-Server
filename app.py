
from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, Blueprint
from werkzeug import secure_filename

from server import app
from ccsm.main_ccsm import ccsm_page, setuser
app.register_blueprint(ccsm_page, url_prefix='/ccsm')

from rf.rforms import rf_page
app.register_blueprint(rf_page, url_prefix='/rf')

from ta.ta import ta_page
app.register_blueprint(ta_page, url_prefix='/ta')

from telephone.telephone import telephone_page
app.register_blueprint(telephone_page, url_prefix='/telephone')

from contingent.contingent import contingent_page
app.register_blueprint(contingent_page, url_prefix='/contingent')

from travel.travel import travel_page
app.register_blueprint(travel_page, url_prefix='/travel')

######################## menu ##############################
@app.route('/select_menu', methods=['POST'])
def select_menu():
    choice = request.form['service']
    if choice == "ccs":
      setuser()
      return redirect(url_for('ccsm_page.start_ccsm'))
    elif choice == "rf":
      return redirect(url_for('rf_page.index'))
    elif choice == "ta":
      return redirect(url_for('ta_page.index'))
    elif choice == "telephone":
      return redirect(url_for('telephone_page.index'))
    elif choice == "contingent":
      return redirect(url_for('contingent_page.index'))
    elif choice == "travel":
      return redirect(url_for('travel_page.index'))
    else:
      return render_template('show_menu.html') 

    # elif choice == "see_db":      
    #   return redirect(url_for('sdb_page.index'))
    # elif choice == "profile":      
    #   return redirect(url_for('profile_page.index'))  
    return page_not_found(".") 
    
    
#################----------------Starts the app--------------##########                                     
if __name__ == '__main__':
   app.run(debug = True)                   #running the app        
