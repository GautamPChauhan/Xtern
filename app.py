# import mysql.connector
# from flask import Flask, request, redirect, url_for, flash, render_template,session
# from modules.company import validate_company_registration,validate_company_login
# from werkzeug.security import generate_password_hash,check_password_hash
# from modules.applicant import validate_applicant_registration,validate_applicant_login
# import os
# from werkzeug.utils import secure_filename


# db_config = {
#     "host": "localhost",
#     "port": 3307,
#     "user": "root",
#     "password": "",
#     "database": "internship_management"
# }

# def get_db_connection():
#     return mysql.connector.connect(**db_config)

# app = Flask(__name__)
# app.secret_key = "f9b2e3a7d9c34e8fa123456789abcdef"

# @app.route('/')
# def home():
#     return render_template('index.html')



# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form_data={}
#     errors={}
#     if request.method == "POST":
#         form_data={
#             'email':request.form.get('email').strip(),
#             'password':request.form.get('password').strip(),
#             'user_type':request.form.get('user_type')
#         }
        
#         if form_data['user_type']=="applicant":
#             errors=validate_applicant_login(form_data)
            
#         elif form_data['user_type']=="company":
#             errors=validate_company_login(form_data)
            
#         if errors:
#             show_alert = True
#             return render_template('login.html', form_data=form_data, errors=errors, show_alert=show_alert)
        
        
#         conn=get_db_connection()
#         cursor=conn.cursor()
        
#         if form_data['user_type']=="applicant":
#             fetch_query="""
#             select * from applicant where email=%s
#             """
#             cursor.execute(fetch_query,(form_data['email'],))
#             result=cursor.fetchone()
            
#             if result:
#                 user_id=result[0]
#                 email=result[5]
#                 password=result[8]
#                 print(password)
#                 is_password_correct=check_password_hash(password,form_data['password'])
#                 print(is_password_correct)
#                 if is_password_correct:
#                     session["user_id"]=user_id
#                     session["email"]=email
#                     return render_template("homepage.html")
#                 else :
#                     password_alert_applicant=True
#                     return render_template('login.html',form_data=form_data,errors=errors,password_alert_applicant=password_alert_applicant)
#             else:
#                 login_alert = True
#                 return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)
        
#         elif form_data['user_type']=="company":
#             fetch_query="""
#             select * from company where email=%s
#             """
#             cursor.execute(fetch_query,(form_data['email'],))
#             result=cursor.fetchone()
            
#             if result:
#                 company_id=result[0]
#                 email=result[2]
#                 password=result[8]
#                 status=result[7]
                
#                 if status != "Approved":
#                     not_approved_alert = True
#                     return render_template('login.html', form_data=form_data, errors=errors, not_approved_alert=not_approved_alert)
                
#                 is_password_correct=check_password_hash(password,form_data['password'])
#                 print(is_password_correct)
#                 if is_password_correct:
#                     session["company_id"]=company_id
#                     session["email"]=email
#                     return render_template("homepage.html")
#                 else :
#                     password_alert_company=True
#                     return render_template('login.html',form_data=form_data,errors=errors,password_alert_company=password_alert_company)
#             else:
#                 login_alert = True
#                 return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

        
#         # print("Login success")
#         # return render_template("homepage.html")
#     return render_template("login.html",form_data=form_data, errors=errors)





# @app.route('/register/company', methods=['GET', 'POST'])
# def register_company():
#     form_data = {}  # Initialize form_data to avoid errors in GET requests
#     errors = {}

#     if request.method == 'POST':
#         print("Form Submitted!")  # Debugging
#         # print(request.form)  

#         form_data = {
#             'company_name': request.form.get('company_name', '').strip(),
#             'industry': request.form.get('industry', '').strip(),
#             'contact_person': request.form.get('contact_person', '').strip(),
#             'email': request.form.get('email', '').strip(),
#             'website_url':request.form.get('website_url','').strip(),
#             'phone': request.form.get('contact_no', '').strip(),
#             'password': request.form.get('password', '').strip(),
#             'confirm_password': request.form.get('confirm_password', '').strip(),
#             'pincode': request.form.get('pincode', '').strip(),
#             'address_line': request.form.get('address_line', '').strip(),
#             'area': request.form.get('area','').strip(),
#             'city': request.form.get('city', '').strip(),
#             'state': request.form.get('state', '').strip(),
#             'address_type':request.form.get('address_type','').strip()
#         }

#         # Validate form data
#         errors = validate_company_registration(form_data)

#         if errors:
#             print("Errors found:")
#             print(errors)
#             show_alert=True
#             return render_template('register_company.html', form_data=form_data, errors=errors,show_alert=show_alert)

#         hashed_password = generate_password_hash(form_data['password'],method="pbkdf2:sha256")
#         print("db time")
#         try:
#             conn=get_db_connection()
#             cursor = conn.cursor()

#             # Insert company data into database
#             insert_query = """
#             INSERT INTO company (company_name,email,contact_person,contact_no,website_url,industry,status,password)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_query, (
#                 form_data['company_name'],form_data['email'],form_data['contact_person'],form_data['phone'],form_data['website_url'] ,
#                 form_data['industry'],"Pending",hashed_password
#             ))

            
#             cursor.execute("SELECT company_id FROM company WHERE email = %s", (form_data['email'],))
#             company_id_list = cursor.fetchone()
#             if company_id_list:  # Ensure that company_id exists
#                 company_id = company_id_list[0]

#                 # Insert into company_address
#                 insert_query_address = """
#                 INSERT INTO company_address (company_id, address_line, area, city, state, pincode,address_type)
#                 VALUES (%s, %s, %s, %s, %s, %s,%s)
#                 """
#                 cursor.execute(insert_query_address, (
#                     company_id, form_data['address_line'], form_data['area'], 
#                     form_data['city'], form_data['state'], form_data['pincode'],form_data['address_type']
#                 ))

#                 conn.commit()  

#                 cursor.close()
#                 conn.close()

#                 # flash("Company registered successfully!", "success")
#                 print("Company registered successfully!")
#                 company_success=True
#                 return render_template('login.html',company_success=company_success,form_data={}, errors={})


#         except mysql.connector.Error as err:
#             print("Database Error:", err)
#             flash("An error occurred while registering. Please try again.", "danger")
#             return render_template('register_company.html', form_data=form_data, errors=errors)

#     return render_template('register_company.html', form_data=form_data, errors=errors)







# UPLOAD_FOLDER = 'static/resumes'
# ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/register/applicant', methods=['GET', 'POST'])
# def register_applicant():
#     form_data = {}
#     errors = {}

#     if request.method == "POST":
#         # Collect form data
#         form_data = {
#             'fname': request.form.get("fname", "").strip(),
#             'lname': request.form.get("lname", "").strip(),
#             'dob': request.form.get("dob", "").strip(),
#             'contact_no': request.form.get("contact_no", "").strip(),
#             'email': request.form.get("email", "").strip(),
#             'city': request.form.get("city", "").strip(),
#             'state': request.form.get("state", "").strip(),
#             'password': request.form.get("password", "").strip(),
#             'confirm_password': request.form.get("confirm_password", "").strip(),
#             'resume_url': ""  # will be filled after upload
#         }

#         resume_file = request.files.get("resume_url")
        
#         # Save resume file if valid
#         if resume_file and resume_file.filename != "":
#             filename = secure_filename(resume_file.filename)
#             extension = filename.rsplit('.', 1)[1].lower()

#             if extension in ALLOWED_EXTENSIONS:
#                 new_filename = f"{form_data['email'].replace('@', '_').replace('.', '_')}.{extension}"

#                 resume_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
#                 resume_file.save(resume_path)
#                 form_data['resume_url'] = resume_path  # Save path for DB
#             else:
#                 errors['resume_url'] = "Resume must be a PDF, DOC, or DOCX file."
#         else:
#             errors['resume_url'] = "Resume file is required."

#         # Run validation
#         validation_errors = validate_applicant_registration(form_data)
#         errors.update(validation_errors)

#         # If errors, render form with messages
#         if errors:
#             show_alert = True
#             return render_template('register_applicant.html', form_data=form_data, errors=errors ,show_alert=show_alert)

        
#         # ✅ If successful, do database insert here
        
#         hashed_password = generate_password_hash(form_data['password'], method='pbkdf2:sha256')
#         print(hashed_password)
#         print("db time")
        
#         conn=get_db_connection()
#         cursor=conn.cursor()
        
#         insert_query="""
#         Insert into applicant(fname,lname,dob,contact_no,email,city,state,password,resume_url)
#         values(%s,%s,%s,%s,%s,%s,%s,%s,%s)
#         """
        
#         cursor.execute(insert_query,(form_data['fname'],form_data['lname'],form_data['dob'],form_data['contact_no'],form_data['email'],form_data['city'],
#                                      form_data['state'],hashed_password,form_data['resume_url']))
        
#         conn.commit()  

#         cursor.close()
#         conn.close()

#         # flash("Applicant registered successfully!", "success")
#         print("Applicant registered successfully!")

#         # flash("Applicant registered successfully!", "success")
#         applicant_success=True
#         return render_template('login.html',applicant_success=applicant_success,form_data={}, errors={})

#     return render_template('register_applicant.html', form_data=form_data, errors=errors)




# @app.route('/about')
# def about():
#     return render_template('about.html')



# @app.route('/contact')
# def contact():
#     return render_template('contact.html')



# if __name__ == '__main__':
#     app.run(debug=True)


# import mysql.connector
# from flask import Flask, request, redirect, url_for, flash, render_template, session
# from modules.company import validate_company_registration, validate_company_login
# from werkzeug.security import generate_password_hash, check_password_hash
# from modules.applicant import validate_applicant_registration, validate_applicant_login
# import os
# from werkzeug.utils import secure_filename


# db_config = {
#     "host": "localhost",
#     "port": 3307,
#     "user": "root",
#     "password": "",
#     "database": "internship_management"
# }

# def get_db_connection():
#     return mysql.connector.connect(**db_config)

# app = Flask(__name__)
# app.secret_key = "f9b2e3a7d9c34e8fa123456789abcdef"

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form_data = {}
#     errors = {}
#     if request.method == "POST":
#         form_data = {
#             'email': request.form.get('email').strip(),
#             'password': request.form.get('password').strip(),
#             'user_type': request.form.get('user_type')
#         }

#         if form_data['user_type'] == "applicant":
#             errors = validate_applicant_login(form_data)
#         elif form_data['user_type'] == "company":
#             errors = validate_company_login(form_data)

#         if errors:
#             show_alert = True
#             return render_template('login.html', form_data=form_data, errors=errors, show_alert=show_alert)

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         if form_data['user_type'] == "applicant":
#             fetch_query = "SELECT * FROM applicant WHERE email=%s"
#             cursor.execute(fetch_query, (form_data['email'],))
#             result = cursor.fetchone()

#             if result:
#                 user_id = result['user_id']
#                 email = result['email']
#                 password = result['password']
#                 is_password_correct = check_password_hash(password, form_data['password'])

#                 if is_password_correct:
#                     session["user_id"] = user_id
#                     session["email"] = email
#                     return render_template("applicant_dashboard.html")
#                 else:
#                     password_alert_applicant = True
#                     return render_template('login.html', form_data=form_data, errors=errors, password_alert_applicant=password_alert_applicant)
#             else:
#                 login_alert = True
#                 return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

#         elif form_data['user_type'] == "company":
#             fetch_query = "SELECT * FROM company WHERE email=%s"
#             cursor.execute(fetch_query, (form_data['email'],))
#             result = cursor.fetchone()

#             if result:
#                 company_id = result['company_id']
#                 email = result['email']
#                 password = result['password']
#                 status = result['status']

#                 if status != "Approved":
#                     not_approved_alert = False
#                     rejected_alert = False

#                     if status == "Rejected":
#                         rejected_alert = True
#                     else:
#                         not_approved_alert = True

#                     return render_template(
#                         'login.html',
#                         form_data=form_data,
#                         errors=errors,
#                         not_approved_alert=not_approved_alert,
#                         rejected_alert=rejected_alert
#                     )

#                 is_password_correct = check_password_hash(password, form_data['password'])

#                 if is_password_correct:
#                     session["company_id"] = company_id
#                     session["email"] = email
#                     return render_template("company_dashboard.html")
#                 else:
#                     password_alert_company = True
#                     return render_template('login.html', form_data=form_data, errors=errors, password_alert_company=password_alert_company)
#             else:
#                 login_alert = True
#                 return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

#     return render_template("login.html", form_data=form_data, errors=errors)

# @app.route('/register/company', methods=['GET', 'POST'])
# def register_company():
#     form_data = {}
#     errors = {}

#     if request.method == 'POST':
#         print("Form Submitted!")

#         form_data = {
#             'company_name': request.form.get('company_name', '').strip(),
#             'industry': request.form.get('industry', '').strip(),
#             'contact_person': request.form.get('contact_person', '').strip(),
#             'email': request.form.get('email', '').strip(),
#             'website_url': request.form.get('website_url', '').strip(),
#             'phone': request.form.get('contact_no', '').strip(),
#             'password': request.form.get('password', '').strip(),
#             'confirm_password': request.form.get('confirm_password', '').strip(),
#             'pincode': request.form.get('pincode', '').strip(),
#             'address_line': request.form.get('address_line', '').strip(),
#             'area': request.form.get('area', '').strip(),
#             'city': request.form.get('city', '').strip(),
#             'state': request.form.get('state', '').strip(),
#             'address_type': request.form.get('address_type', '').strip()
#         }

#         errors = validate_company_registration(form_data)

#         if errors:
#             print("Errors found:")
#             print(errors)
#             show_alert = True
#             return render_template('register_company.html', form_data=form_data, errors=errors, show_alert=show_alert)

#         hashed_password = generate_password_hash(form_data['password'], method="pbkdf2:sha256")
#         print("db time")
#         try:
#             conn = get_db_connection()
#             cursor = conn.cursor(dictionary=True)

#             insert_query = """
#             INSERT INTO company (company_name, email, contact_person, contact_no, website_url, industry, status, password)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#             """
#             cursor.execute(insert_query, (
#                 form_data['company_name'], form_data['email'], form_data['contact_person'],
#                 form_data['phone'], form_data['website_url'], form_data['industry'],
#                 "Pending", hashed_password
#             ))

#             cursor.execute("SELECT company_id FROM company WHERE email = %s", (form_data['email'],))
#             company_id_row = cursor.fetchone()
#             if company_id_row:
#                 company_id = company_id_row['company_id']

#                 insert_query_address = """
#                 INSERT INTO company_address (company_id, address_line, area, city, state, pincode, address_type)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(insert_query_address, (
#                     company_id, form_data['address_line'], form_data['area'],
#                     form_data['city'], form_data['state'], form_data['pincode'],
#                     form_data['address_type']
#                 ))

#                 conn.commit()
#                 cursor.close()
#                 conn.close()

#                 print("Company registered successfully!")
#                 company_success = True
#                 return render_template('login.html', company_success=company_success, form_data={}, errors={})

#         except mysql.connector.Error as err:
#             print("Database Error:", err)
#             flash("An error occurred while registering. Please try again.", "danger")
#             return render_template('register_company.html', form_data=form_data, errors=errors)

#     return render_template('register_company.html', form_data=form_data, errors=errors)

# UPLOAD_FOLDER = 'static/resumes'
# ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/register/applicant', methods=['GET', 'POST'])
# def register_applicant():
#     form_data = {}
#     errors = {}

#     if request.method == "POST":
#         form_data = {
#             'fname': request.form.get("fname", "").strip(),
#             'lname': request.form.get("lname", "").strip(),
#             'dob': request.form.get("dob", "").strip(),
#             'contact_no': request.form.get("contact_no", "").strip(),
#             'email': request.form.get("email", "").strip(),
#             'city': request.form.get("city", "").strip(),
#             'state': request.form.get("state", "").strip(),
#             'password': request.form.get("password", "").strip(),
#             'confirm_password': request.form.get("confirm_password", "").strip(),
#             'resume_url': ""
#         }

#         resume_file = request.files.get("resume_url")

#         if resume_file and resume_file.filename != "":
#             filename = secure_filename(resume_file.filename)
#             extension = filename.rsplit('.', 1)[1].lower()

#             if extension in ALLOWED_EXTENSIONS:
#                 new_filename = f"{form_data['email'].replace('@', '_').replace('.', '_')}.{extension}"
#                 resume_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
#                 resume_file.save(resume_path)
#                 form_data['resume_url'] = resume_path
#             else:
#                 errors['resume_url'] = "Resume must be a PDF, DOC, or DOCX file."
#         else:
#             errors['resume_url'] = "Resume file is required."

#         validation_errors = validate_applicant_registration(form_data)
#         errors.update(validation_errors)

#         if errors:
#             show_alert = True
#             return render_template('register_applicant.html', form_data=form_data, errors=errors, show_alert=show_alert)

#         hashed_password = generate_password_hash(form_data['password'], method='pbkdf2:sha256')
#         print(hashed_password)
#         print("db time")

#         conn = get_db_connection()
#         cursor = conn.cursor(dictionary=True)

#         insert_query = """
#         INSERT INTO applicant (fname, lname, dob, contact_no, email, city, state, password, resume_url)
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """

#         cursor.execute(insert_query, (
#             form_data['fname'], form_data['lname'], form_data['dob'], form_data['contact_no'],
#             form_data['email'], form_data['city'], form_data['state'],
#             hashed_password, form_data['resume_url']
#         ))

#         conn.commit()
#         cursor.close()
#         conn.close()

#         print("Applicant registered successfully!")
#         applicant_success = True
#         return render_template('login.html', applicant_success=applicant_success, form_data={}, errors={})

#     return render_template('register_applicant.html', form_data=form_data, errors=errors)




# @app.route('/admin/dashboard')
# def admin_dashboard():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)

#     # Fetch companies that are pending approval
#     cursor.execute("SELECT * FROM company WHERE status = 'Pending'")
#     pending_companies = cursor.fetchall()

#     # Fetch all applicants
#     # cursor.execute("SELECT * FROM applicant")
#     # applicants = cursor.fetchall()

#     # Fetch all internships
#     cursor.execute("SELECT * FROM internship")
#     internships = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     return render_template('admin_dashboard.html',
#                            pending_companies=pending_companies,
#                         #    applicants=applicants,
#                            internships=internships)


# @app.route('/admin/company/<int:company_id>/<action>', methods=['POST'])
# def handle_company_approval(company_id, action):
#     if action not in ['approve', 'reject']:
#         flash("Invalid action.", "danger")
#         return redirect(url_for('admin_dashboard'))

#     new_status = 'Approved' if action == 'approve' else 'Rejected'

#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("UPDATE company SET status = %s WHERE company_id = %s", (new_status, company_id))
#     conn.commit()
#     cursor.close()
#     conn.close()

#     flash(f"Company {new_status.lower()} successfully!", "success")
#     return redirect(url_for('admin_dashboard'))


# # View all companies
# @app.route('/admin/companies')
# def view_companies():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM company where status='Approved' ")
#     approved = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('approved_companies.html', approved=approved)

# # View all applicants
# @app.route('/admin/applicants')
# def view_applicants():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM applicant")
#     applicants = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('applicants.html', applicants=applicants)

# @app.route('/admin/pending_companies')
# def pending_companies():
#     conn = get_db_connection()
#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM company WHERE status = 'Pending'")
#     pending_companies = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return render_template('pending_companies.html', pending_companies=pending_companies)

# # Analytics (You can fill it with graphs/statistics later)
# @app.route('/admin/analytics')
# def analytics():
#     return render_template('analytics.html')

# # Reports (Simple placeholder for now)
# @app.route('/admin/reports')
# def reports():
#     return render_template('reports.html')

# # Log out (this depends on how you're handling sessions)
# @app.route('/logout')
# def logout():
#     session.clear()
#     # flash("You’ve been logged out.", "info")
#     return redirect(url_for('login'))



# @app.route('/about')
# def about():
#     return render_template('about.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')


# @app.route('/applicant/dashboard')
# def applicant_dashboard():
#     if 'user_id' not in session:
#         # flash("Please log in as applicant to access your dashboard.", "warning")
#         return redirect(url_for('login'))

#     # user_id = session['user_id']

#     # # Fetch applicant details (optional)
#     # conn = get_db_connection()
#     # cursor = conn.cursor(dictionary=True)

#     # cursor.execute("SELECT * FROM applicant WHERE user_id = %s", (user_id,))
#     # applicant = cursor.fetchone()

#     # cursor.close()
#     # conn.close()

#     return render_template('applicant_dashboard.html', applicant=applicant)


# if __name__ == '__main__':
#     app.run(debug=True)


import mysql.connector
from flask import Flask, request, redirect, url_for, flash, render_template, session
from modules.company import validate_company_registration, validate_company_login
from werkzeug.security import generate_password_hash, check_password_hash
from modules.applicant import validate_applicant_registration, validate_applicant_login
import os
from werkzeug.utils import secure_filename


db_config = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "internship_management"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

app = Flask(__name__)
app.secret_key = "f9b2e3a7d9c34e8fa123456789abcdef"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    form_data = {}
    errors = {}
    if request.method == "POST":
        form_data = {
            'email': request.form.get('email').strip(),
            'password': request.form.get('password').strip(),
            'user_type': request.form.get('user_type')
        }

        if form_data['user_type'] == "applicant":
            errors = validate_applicant_login(form_data)
        elif form_data['user_type'] == "company":
            errors = validate_company_login(form_data)

        if errors:
            show_alert = True
            return render_template('login.html', form_data=form_data, errors=errors, show_alert=show_alert)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if form_data['user_type'] == "applicant":
            fetch_query = "SELECT * FROM applicant WHERE email=%s"
            cursor.execute(fetch_query, (form_data['email'],))
            result = cursor.fetchone()

            if result:
                user_id = result['user_id']
                email = result['email']
                password = result['password']
                is_password_correct = check_password_hash(password, form_data['password'])

                if is_password_correct:
                    session["user_id"] = user_id
                    session["email"] = email
                    return render_template("applicant_dashboard.html")
                else:
                    password_alert_applicant = True
                    return render_template('login.html', form_data=form_data, errors=errors, password_alert_applicant=password_alert_applicant)
            else:
                login_alert = True
                return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

        elif form_data['user_type'] == "company":
            fetch_query = "SELECT * FROM company WHERE email=%s"
            cursor.execute(fetch_query, (form_data['email'],))
            result = cursor.fetchone()

            if result:
                company_id = result['company_id']
                email = result['email']
                password = result['password']
                status = result['status']

                if status != "Approved":
                    not_approved_alert = False
                    rejected_alert = False

                    if status == "Rejected":
                        rejected_alert = True
                    else:
                        not_approved_alert = True

                    return render_template(
                        'login.html',
                        form_data=form_data,
                        errors=errors,
                        not_approved_alert=not_approved_alert,
                        rejected_alert=rejected_alert
                    )

                is_password_correct = check_password_hash(password, form_data['password'])

                if is_password_correct:
                    session["company_id"] = company_id
                    session["email"] = email
                    return render_template("company_dashboard.html")
                else:
                    password_alert_company = True
                    return render_template('login.html', form_data=form_data, errors=errors, password_alert_company=password_alert_company)
            else:
                login_alert = True
                return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

    return render_template("login.html", form_data=form_data, errors=errors)

@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    form_data = {}
    errors = {}

    if request.method == 'POST':
        print("Form Submitted!")

        form_data = {
            'company_name': request.form.get('company_name', '').strip(),
            'industry': request.form.get('industry', '').strip(),
            'contact_person': request.form.get('contact_person', '').strip(),
            'email': request.form.get('email', '').strip(),
            'website_url': request.form.get('website_url', '').strip(),
            'phone': request.form.get('contact_no', '').strip(),
            'password': request.form.get('password', '').strip(),
            'confirm_password': request.form.get('confirm_password', '').strip(),
            'pincode': request.form.get('pincode', '').strip(),
            'address_line': request.form.get('address_line', '').strip(),
            'area': request.form.get('area', '').strip(),
            'city': request.form.get('city', '').strip(),
            'state': request.form.get('state', '').strip(),
            'address_type': request.form.get('address_type', '').strip()
        }

        errors = validate_company_registration(form_data)

        if errors:
            print("Errors found:")
            print(errors)
            show_alert = True
            return render_template('register_company.html', form_data=form_data, errors=errors, show_alert=show_alert)

        hashed_password = generate_password_hash(form_data['password'], method="pbkdf2:sha256")
        print("db time")
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            insert_query = """
            INSERT INTO company (company_name, email, contact_person, contact_no, website_url, industry, status, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                form_data['company_name'], form_data['email'], form_data['contact_person'],
                form_data['phone'], form_data['website_url'], form_data['industry'],
                "Pending", hashed_password
            ))

            cursor.execute("SELECT company_id FROM company WHERE email = %s", (form_data['email'],))
            company_id_row = cursor.fetchone()
            if company_id_row:
                company_id = company_id_row['company_id']

                insert_query_address = """
                INSERT INTO company_address (company_id, address_line, area, city, state, pincode, address_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query_address, (
                    company_id, form_data['address_line'], form_data['area'],
                    form_data['city'], form_data['state'], form_data['pincode'],
                    form_data['address_type']
                ))

                conn.commit()
                cursor.close()
                conn.close()

                print("Company registered successfully!")
                company_success = True
                return render_template('login.html', company_success=company_success, form_data={}, errors={})

        except mysql.connector.Error as err:
            print("Database Error:", err)
            flash("An error occurred while registering. Please try again.", "danger")
            return render_template('register_company.html', form_data=form_data, errors=errors)

    return render_template('register_company.html', form_data=form_data, errors=errors)

UPLOAD_FOLDER = 'static/resumes'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/register/applicant', methods=['GET', 'POST'])
def register_applicant():
    form_data = {}
    errors = {}

    if request.method == "POST":
        form_data = {
            'fname': request.form.get("fname", "").strip(),
            'lname': request.form.get("lname", "").strip(),
            'dob': request.form.get("dob", "").strip(),
            'contact_no': request.form.get("contact_no", "").strip(),
            'email': request.form.get("email", "").strip(),
            'city': request.form.get("city", "").strip(),
            'state': request.form.get("state", "").strip(),
            'password': request.form.get("password", "").strip(),
            'confirm_password': request.form.get("confirm_password", "").strip(),
            'resume_url': ""
        }

        resume_file = request.files.get("resume_url")

        if resume_file and resume_file.filename != "":
            filename = secure_filename(resume_file.filename)
            extension = filename.rsplit('.', 1)[1].lower()

            if extension in ALLOWED_EXTENSIONS:
                new_filename = f"{form_data['email'].replace('@', '_').replace('.', '_')}.{extension}"
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                resume_file.save(resume_path)
                form_data['resume_url'] = resume_path
            else:
                errors['resume_url'] = "Resume must be a PDF, DOC, or DOCX file."
        else:
            errors['resume_url'] = "Resume file is required."

        validation_errors = validate_applicant_registration(form_data)
        errors.update(validation_errors)

        if errors:
            show_alert = True
            return render_template('register_applicant.html', form_data=form_data, errors=errors, show_alert=show_alert)

        hashed_password = generate_password_hash(form_data['password'], method='pbkdf2:sha256')
        print(hashed_password)
        print("db time")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        insert_query = """
        INSERT INTO applicant (fname, lname, dob, contact_no, email, city, state, password, resume_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            form_data['fname'], form_data['lname'], form_data['dob'], form_data['contact_no'],
            form_data['email'], form_data['city'], form_data['state'],
            hashed_password, form_data['resume_url']
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print("Applicant registered successfully!")
        applicant_success = True
        return render_template('login.html', applicant_success=applicant_success, form_data={}, errors={})

    return render_template('register_applicant.html', form_data=form_data, errors=errors)




@app.route('/admin/dashboard')
def admin_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch companies that are pending approval
    cursor.execute("SELECT * FROM company WHERE status = 'Pending'")
    pending_companies = cursor.fetchall()

    # Fetch all applicants
    # cursor.execute("SELECT * FROM applicant")
    # applicants = cursor.fetchall()

    # Fetch all internships
    cursor.execute("SELECT * FROM internship")
    internships = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_dashboard.html',
                           pending_companies=pending_companies,
                        #    applicants=applicants,
                           internships=internships)


@app.route('/admin/company/<int:company_id>/<action>', methods=['POST'])
def handle_company_approval(company_id, action):
    if action not in ['approve', 'reject']:
        flash("Invalid action.", "danger")
        return redirect(url_for('admin_dashboard'))

    new_status = 'Approved' if action == 'approve' else 'Rejected'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE company SET status = %s WHERE company_id = %s", (new_status, company_id))
    conn.commit()
    cursor.close()
    conn.close()

    flash(f"Company {new_status.lower()} successfully!", "success")
    return redirect(url_for('admin_dashboard'))


# View all companies
@app.route('/admin/companies')
def view_companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM company where status='Approved' ")
    approved = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('approved_companies.html', approved=approved)

# View all applicants
@app.route('/admin/applicants')
def view_applicants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant")
    applicants = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('applicants.html', applicants=applicants)

@app.route('/admin/pending_companies')
def pending_companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM company WHERE status = 'Pending'")
    pending_companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pending_companies.html', pending_companies=pending_companies)

# Analytics (You can fill it with graphs/statistics later)
@app.route('/admin/analytics')
def analytics():
    return render_template('analytics.html')

# Reports (Simple placeholder for now)
@app.route('/admin/reports')
def reports():
    return render_template('reports.html')

# Log out (this depends on how you're handling sessions)
@app.route('/logout')
def logout():
    session.clear()
    # flash("You’ve been logged out.", "info")
    return redirect(url_for('login'))



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/applicant/dashboard')
def applicant_dashboard():
    user_id = session.get('user_id')

    if not user_id:
        return redirect(url_for('applicant_login'))  # Redirect to login if session not present

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the user has submitted qualifications
    cursor.execute("SELECT * FROM user_qualification WHERE user_id = %s", (user_id,))
    qualification = cursor.fetchone()

    cursor.close()
    conn.close()

    has_qualification = qualification is not None

    return render_template('applicant_dashboard.html', has_qualification=has_qualification)



@app.route('/applicant/add_qualification', methods=['GET', 'POST'])
def add_qualification():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch available degrees
    cursor.execute("SELECT * FROM degree")
    degrees = cursor.fetchall()

    if request.method == 'POST':
        degree_id = request.form['degree_id']
        year = request.form['year']
        board = request.form['board']
        percentage = request.form['percentage']
        main_subjects = request.form['main_subjects']
        sub_subjects = request.form['sub_subjects']
        skills = request.form['skills']
        interest = request.form['interest']
        institute = request.form['institute']

        # Insert the qualification
        cursor.execute("""
            INSERT INTO user_qualification (
                user_id, degree_id, year, board, percentage,
                main_subjects, sub_subjects, skills, interest, institute
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, degree_id, year, board, percentage,
              main_subjects, sub_subjects, skills, interest, institute))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('applicant_dashboard'))

    cursor.close()
    conn.close()
    return render_template('add_qualification.html', degrees=degrees)



@app.route('/applicant/my_qualifications')
def applicant_myqualifications():
    user_id = session.get('user_id')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT uq.*, d.degree_name FROM user_qualification uq
        JOIN degree d ON uq.degree_id = d.degree_id
        WHERE uq.user_id = %s
    """
    cursor.execute(query, (user_id,))
    qualification = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('applicant_myqualifications.html', qualification=qualification)



if __name__ == '__main__':
    app.run(debug=True)
