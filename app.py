
import mysql.connector
from flask import Flask, request, redirect, url_for, flash, render_template, session,jsonify,Blueprint,send_from_directory
from modules.company import validate_company_registration, validate_company_login
from werkzeug.security import generate_password_hash, check_password_hash
from modules.applicant import validate_applicant_registration, validate_applicant_login
from modules.send_email import send_email
import os
from werkzeug.utils import secure_filename
from datetime import date,timedelta
from collections import defaultdict
import calendar
from collections import Counter
from datetime import datetime
from decimal import Decimal
import logging
import yagmail
import random
import string
import time


app = Flask(__name__)
app.secret_key = "f9b2e3a7d9c34e8fa123456789abcdef"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # Session expires after 10 minutes

db_config = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "internship_management"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)




@app.route('/')
def home():
    return render_template('index.html')



@app.route('/admin/login', methods=["GET", "POST"])
def admin_login():
    form_data = {}
    errors = {}
    show_alert = False

    if request.method == "POST":
        form_data = {
            'email': request.form.get('email').strip(),
            'password': request.form.get('password').strip()
        }

        # Basic validation
        if not form_data['email']:
            errors['email'] = 'Email is required.'
        if not form_data['password']:
            errors['password'] = 'Password is required.'

        if errors:
            show_alert = True
            return render_template('admin_login.html', form_data=form_data, errors=errors, show_alert=show_alert)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Query admin table
        fetch_query = "SELECT * FROM admin WHERE email=%s"
        cursor.execute(fetch_query, (form_data['email'],))
        result = cursor.fetchone()

        conn.close()

        if result:
            admin_id = result['admin_id']
            email = result['email']
            password = result['password']
            is_password_correct = check_password_hash(password, form_data['password'])

            if is_password_correct:
                session["admin_id"] = admin_id
                session["email"] = email
                return redirect(url_for("admin_dashboard"))  # Adjust to your admin dashboard route
            else:
                show_alert = True
                errors['password'] = 'Incorrect password.'
        else:
            show_alert = True
            errors['email'] = 'Admin email not found.'

        return render_template('admin_login.html', form_data=form_data, errors=errors, show_alert=show_alert)

    return render_template("admin_login.html", form_data=form_data, errors=errors)




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
                    return redirect(url_for("applicant_dashboard"))

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
                    return redirect(url_for("company_dashboard"))
                else:
                    password_alert_company = True
                    return render_template('login.html', form_data=form_data, errors=errors, password_alert_company=password_alert_company)
            else:
                login_alert = True
                return render_template('login.html', form_data=form_data, errors=errors, login_alert=login_alert)

    return render_template("login.html", form_data=form_data, errors=errors)




# Email sending function
def send_verification_email(to: str, code: str) -> bool:
    try:
        email_user = 'www.gautam.2005@gmail.com'
        email_pass = 'iqva ossc swsh znsg'  # App password
        yag = yagmail.SMTP(email_user, email_pass)
        subject = "Xtern Password Reset Verification Code"
        content = f"""
        <h2>Xtern Password Reset</h2>
        <p>Your verification code is: <strong>{code}</strong></p>
        <p>This code is valid for 10 minutes. Please enter it to reset your password.</p>
        """
        yag.send(to=to, subject=subject, contents=[yagmail.inline(content)])
        print(f"[✓] Verification email sent to {to}")
        return True
    except Exception as e:
        print(f"[✗] Failed to send email to {to}: {e}")
        return False

# Generate a random 6-digit verification code
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Validate email and user_type
def validate_forgot_password_form(form_data):
    errors = {}
    if not form_data['email']:
        errors['email'] = "Email is required."
    elif '@' not in form_data['email']:
        errors['email'] = "Invalid email format."
    if not form_data['user_type']:
        errors['user_type'] = "Please select a user type."
    elif form_data['user_type'] not in ['applicant', 'company']:
        errors['user_type'] = "Invalid user type."
    return errors

# Validate verification code
def validate_verification_code_form(form_data):
    errors = {}
    if not form_data['code']:
        errors['code'] = "Verification code is required."
    return errors

# Validate reset password form
def validate_reset_password_form(form_data):
    errors = {}
    if not form_data['password']:
        errors['password'] = "Password is required."
    elif len(form_data['password']) < 6:
        errors['password'] = "Password must be at least 6 characters long."
    if not form_data['confirm_password']:
        errors['confirm_password'] = "Please confirm your password."
    elif form_data['password'] != form_data['confirm_password']:
        errors['confirm_password'] = "Passwords do not match."
    return errors

# Forgot Password Route
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form_data = {}
    errors = {}
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email', '').strip(),
            'user_type': request.form.get('user_type', '')
        }
        errors = validate_forgot_password_form(form_data)

        if not errors:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            if form_data['user_type'] == 'applicant':
                query = "SELECT user_id, email FROM applicant WHERE email = %s"
            else:  # company
                query = "SELECT company_id, email, status FROM company WHERE email = %s"
            cursor.execute(query, (form_data['email'],))
            user = cursor.fetchone()
            conn.close()

            if user:
                if form_data['user_type'] == 'company' and user['status'] != 'Approved':
                    if user['status'] == 'Rejected':
                        return render_template('forgot_password.html', form_data=form_data, errors=errors, rejected_alert=True)
                    else:
                        return render_template('forgot_password.html', form_data=form_data, errors=errors, not_approved_alert=True)

                # Generate and store verification code
                code = generate_verification_code()
                session['reset_email'] = form_data['email']
                session['reset_user_type'] = form_data['user_type']
                session['verification_code'] = code
                session['code_expiry'] = time.time() + 600  # 10 minutes expiry
                session.permanent = True

                # Send email and redirect to verify code page
                if send_verification_email(form_data['email'], code):
                    flash("A verification code has been sent to your email.")
                    return redirect(url_for('verify_code'))
                else:
                    errors['email'] = "Failed to send verification email. Please try again."
            else:
                return render_template('forgot_password.html', form_data=form_data, errors=errors, email_error=True)

    return render_template('forgot_password.html', form_data=form_data, errors=errors)

# Verify Code Route
@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if 'reset_email' not in session or 'verification_code' not in session:
        flash("Session expired or invalid. Please start the password reset process again.")
        return redirect(url_for('forgot_password'))

    form_data = {}
    errors = {}
    if request.method == 'POST':
        form_data = {
            'code': request.form.get('code', '').strip()
        }
        errors = validate_verification_code_form(form_data)

        if not errors:
            if time.time() > session.get('code_expiry', 0):
                flash("Verification code has expired. Please request a new one.")
                return redirect(url_for('forgot_password'))

            if form_data['code'] == session['verification_code']:
                return redirect(url_for('reset_password'))
            else:
                errors['code'] = "Invalid verification code."
                return render_template('verify_code.html', form_data=form_data, errors=errors, code_error=True)

    return render_template('verify_code.html', form_data=form_data, errors=errors)

# Reset Password Route
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session or 'reset_user_type' not in session:
        flash("Session expired or invalid. Please start the password reset process again.")
        return redirect(url_for('forgot_password'))

    form_data = {}
    errors = {}
    if request.method == 'POST':
        form_data = {
            'password': request.form.get('password', '').strip(),
            'confirm_password': request.form.get('confirm_password', '').strip()
        }
        errors = validate_reset_password_form(form_data)

        if not errors:
            conn = get_db_connection()
            cursor = conn.cursor()
            hashed_password = generate_password_hash(form_data['password'], method='pbkdf2:sha256', salt_length=8)
            if session['reset_user_type'] == 'applicant':
                query = "UPDATE applicant SET password = %s WHERE email = %s"
            else:  # company
                query = "UPDATE company SET password = %s WHERE email = %s"
            cursor.execute(query, (hashed_password, session['reset_email']))
            conn.commit()
            conn.close()

            # Clear session
            session.pop('reset_email', None)
            session.pop('reset_user_type', None)
            session.pop('verification_code', None)
            session.pop('code_expiry', None)

            flash("Password updated successfully. Please login.")
            return redirect(url_for('login'))

    return render_template('reset_password.html', form_data=form_data, errors=errors)




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

                # ✅ Send confirmation email after successful registration
                subject = "Xtern: Company Registration Received"
                content = f"""
Dear {form_data['contact_person']},

Thank you for registering your company <b>{form_data['company_name']}</b> on Xtern.

Your application is currently under review. You will receive another email once it is approved or rejected by the administrator.

Best regards,<br>
Xtern Team
"""
                send_email(
                    to=form_data['email'],
                    subject=subject,
                    content=content,
                    is_html=True
                )

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

        # ✅ Send email to the applicant after registration
        subject = "Xtern: Applicant Registration Successful"
        content = f"""
Dear {form_data['fname']} {form_data['lname']},

Thank you for registering as an applicant on <b>Xtern</b>.

Your account has been successfully created. You can now log in and complete your profile and start applying to internships.

If you have any questions, feel free to contact us.

Best regards,<br>
Xtern Team
"""
        send_email(
            to=form_data['email'],
            subject=subject,
            content=content,
            is_html=True
        )

        print("Applicant registered successfully!")
        applicant_success = True
        return render_template('login.html', applicant_success=applicant_success, form_data={}, errors={})

    return render_template('register_applicant.html', form_data=form_data, errors=errors)




@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch companies that are pending approval
        cursor.execute("SELECT company_id, company_name, industry, website_url FROM company WHERE status = 'Pending'")
        pending_companies = cursor.fetchall()

        # Fetch approved companies with stats
        cursor.execute("""
            SELECT 
                c.company_id,
                c.company_name,
                COUNT(DISTINCT i.internship_id) AS internship_count,
                COUNT(a.application_id) AS total_applications,
                SUM(CASE WHEN a.status = 'Approved' THEN 1 ELSE 0 END) AS approved_applications,
                SUM(CASE WHEN a.status = 'Pending' THEN 1 ELSE 0 END) AS pending_applications
            FROM company c
            LEFT JOIN internship i ON c.company_id = i.company_id
            LEFT JOIN applications a ON i.internship_id = a.internship_id
            WHERE c.status = 'Approved'
            GROUP BY c.company_id, c.company_name
        """)
        companies = cursor.fetchall()

        # Fetch students with stats, ordered by creation date
        cursor.execute("""
            SELECT 
                a.user_id,
                CONCAT(a.fname, ' ', a.lname) AS student_name,
                COUNT(DISTINCT app.application_id) AS application_count,
                SUM(CASE WHEN app.status = 'Approved' THEN 1 ELSE 0 END) AS approved_applications,
                SUM(CASE WHEN app.status = 'Pending' THEN 1 ELSE 0 END) AS pending_applications
            FROM applicant a
            LEFT JOIN applications app ON a.user_id = app.user_id
            GROUP BY a.user_id, a.fname, a.lname
            ORDER BY a.user_id DESC  -- Assuming no created_at; replace with a.created_at DESC if available
        """)
        students = cursor.fetchall()

        # Fetch company feedback
        cursor.execute("""
            SELECT 
                f.feedback_id,
                c.company_name,
                f.feedback_text AS comment,
                f.rating,
                f.date_given AS date
            FROM feedback f
            JOIN company c ON f.company_id = c.company_id
            WHERE f.given_by = 'company' AND f.user_id IS NULL
            ORDER BY f.date_given DESC
            LIMIT 5
        """)
        company_feedbacks = cursor.fetchall()

        # Fetch student feedback
        cursor.execute("""
            SELECT 
                f.feedback_id,
                CONCAT(a.fname, ' ', a.lname) AS student_name,
                f.feedback_text AS comment,
                f.rating,
                f.date_given AS date,
                COALESCE(d.degree_name, 'Unknown') AS course
            FROM feedback f
            JOIN applicant a ON f.user_id = a.user_id
            LEFT JOIN (
                SELECT uq.user_id, uq.degree_id
                FROM user_qualification uq
                JOIN (
                    SELECT user_id, MAX(degree_id) AS max_degree_id
                    FROM user_qualification
                    GROUP BY user_id
                ) uq_max ON uq.user_id = uq_max.user_id AND uq.degree_id = uq_max.max_degree_id
            ) uq_filtered ON a.user_id = uq_filtered.user_id
            LEFT JOIN degree d ON uq_filtered.degree_id = d.degree_id
            WHERE f.given_by = 'applicant' AND f.company_id IS NULL
            ORDER BY f.date_given DESC
            LIMIT 5;

        """)
        student_feedbacks = cursor.fetchall()

        return render_template('admin_dashboard.html',
                               pending_companies=pending_companies,
                               companies=companies,
                               students=students,
                               company_feedbacks=company_feedbacks,
                               student_feedbacks=student_feedbacks)

    except mysql.connector.Error as err:
        # Database error
        return render_template('admin_dashboard.html', error=f"Database error: {err}",
                               pending_companies=[], companies=[], students=[],
                               company_feedbacks=[], student_feedbacks=[]), 500
    except Exception as e:
        # Unexpected error
        return render_template('admin_dashboard.html', error=f"An unexpected error occurred: {e}",
                               pending_companies=[], companies=[], students=[],
                               company_feedbacks=[], student_feedbacks=[]), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
            

@app.route('/admin/company/<int:company_id>/<action>', methods=['POST'])
def handle_company_approval(company_id, action):
    
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    if action not in ['approve', 'reject']:
        flash("Invalid action.", "danger")
        return redirect(url_for('admin_dashboard'))

    new_status = 'Approved' if action == 'approve' else 'Rejected'

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Update status in the database
    cursor.execute("UPDATE company SET status = %s WHERE company_id = %s", (new_status, company_id))
    conn.commit()

    # Fetch company name and email
    cursor.execute("SELECT company_name, email FROM company WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()

    cursor.close()
    conn.close()

    # Prepare email content
    if company:
        subject = f"Your company has been {new_status} on Xtern"
        if new_status == 'Approved':
            content = f"""
            Dear {company['company_name']},

            Congratulations! Your company registration on Xtern has been approved. 
            You can now log in to your dashboard and start posting internships.

            Regards,
            Xtern Admin Team
            """
        else:
            content = f"""
            Dear {company['company_name']},

            We regret to inform you that your company registration on Xtern has been rejected.
            For further inquiries, please contact support.

            Regards,
            Xtern Admin Team
            """

        send_email(to=company['email'], subject=subject, content=content)

    flash(f"Company {new_status.lower()} successfully!", "success")
    return redirect(url_for('admin_dashboard'))


# View all companies
@app.route('/admin/companies')
def view_companies():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
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
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applicant")
    applicants = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_applicants.html', applicants=applicants)

@app.route('/admin/pending_companies')
def pending_companies():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM company WHERE status = 'Pending'")
    pending_companies = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pending_companies.html', pending_companies=pending_companies)






# Log out (this depends on how you're handling sessions)
@app.route('/logout')
def logout():
    session.clear()
    # flash("You’ve been logged out.", "info")
    return redirect(url_for('login'))




@app.route('/admin_update_internship_status')
def admin_update_internship_status():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Update internships where closed_date is past and status is not already closed
        query = """
            UPDATE internship
            SET status = 'closed', internship_status = 'closed'
            WHERE close_date < %s 
            AND status != 'closed'
            AND close_date IS NOT NULL
        """
        today = date.today()
        cursor.execute(query, (today,))
        conn.commit()

        # Get the number of affected rows for feedback
        updated_count = cursor.rowcount

        # Fetch all closed internships with additional details
        cursor.execute("""
            SELECT 
                i.internship_id, 
                i.title, 
                i.close_date, 
                i.status, 
                i.internship_status,
                i.open_date,
                i.duration,
                i.location,
                i.job_offer,
                c.company_name
            FROM internship i
            JOIN company c ON i.company_id = c.company_id
            WHERE i.status = 'closed' AND i.internship_status = 'closed'
        """)
        closed_internships = cursor.fetchall()

        # Render the template with success notification
        return render_template('admin_update_internship_status.html',
                               updated_count=updated_count,
                               closed_internships=closed_internships,
                               message=f"Successfully updated {updated_count} internship(s) to closed status.")

    except mysql.connector.Error as err:
        # Log error and render template with error message
        print(f"Database error: {err}")
        return render_template('admin_update_internship_status.html',
                               updated_count=0,
                               closed_internships=[],
                               error=f"Database error: {err}"), 500

    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()            
            

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')





# Assuming get_db_connection is defined elsewhere
# from . import get_db_connection

@app.route('/applicant/dashboard')
def applicant_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('login'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch applicant name
        cursor.execute("SELECT CONCAT(fname, ' ', lname) AS name FROM applicant WHERE user_id = %s", (user_id,))
        applicant = cursor.fetchone()
        applicant_name = applicant['name'] if applicant else 'Unknown User'

        # Check if qualifications exist
        cursor.execute("SELECT * FROM user_qualification WHERE user_id = %s", (user_id,))
        qualifications = cursor.fetchall()  # Use fetchall to consume all results
        has_qualification = len(qualifications) > 0

        # Fetch all unique skills
        cursor.execute("""
            SELECT required_skills, main_subjects, minor_subjects
            FROM internship
            WHERE internship_status = 'open' AND status IN ('open', 'reopen')
        """)
        skill_rows = cursor.fetchall()
        all_skills = set()
        for row in skill_rows:
            for field in ['required_skills', 'main_subjects', 'minor_subjects']:
                if row[field]:
                    skills = [s.strip().lower() for s in row[field].split(',')]
                    all_skills.update(skills)
        all_skills = sorted(list(all_skills))

        internships = []
        if has_qualification:
            cursor.execute("""
                SELECT i.*, c.company_name, c.website_url
                FROM internship i
                JOIN company c ON i.company_id = c.company_id
                WHERE i.internship_status = 'open' AND i.status IN ('open', 'reopen')
            """)
            internships = cursor.fetchall()

            for internship in internships:
                cursor.execute("""
                    SELECT status FROM applications
                    WHERE user_id = %s AND internship_id = %s
                    ORDER BY applied_on DESC LIMIT 1
                """, (user_id, internship['internship_id']))
                application = cursor.fetchone()
                internship['applied'] = bool(application)
                internship['application_status'] = application['status'] if application else None

        return render_template('applicant_dashboard.html',
                               applicant_name=applicant_name,
                               has_qualification=has_qualification,
                               internships=internships,
                               all_skills=all_skills,
                               selected_skills=[])

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('applicant_dashboard.html',
                               applicant_name='Unknown User',
                               has_qualification=False,
                               internships=[],
                               all_skills=[],
                               selected_skills=[],
                               error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('applicant_dashboard.html',
                               applicant_name='Unknown User',
                               has_qualification=False,
                               internships=[],
                               all_skills=[],
                               selected_skills=[],
                               error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



@app.route('/applicant/search_internships', methods=['POST'])
def search_internships():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)  # Add buffered=True

        # Get applicant name
        cursor.execute("SELECT CONCAT(fname, ' ', lname) AS name FROM applicant WHERE user_id = %s", (user_id,))
        applicant = cursor.fetchone()
        applicant_name = applicant['name'] if applicant else 'Unknown User'

        # Check if qualifications are submitted
        cursor.execute("SELECT * FROM user_qualification WHERE user_id = %s", (user_id,))
        qualifications = cursor.fetchall()  # Use fetchall
        has_qualification = len(qualifications) > 0

        # Fetch all unique skills
        cursor.execute("""
            SELECT required_skills, main_subjects, minor_subjects
            FROM internship
            WHERE internship_status = 'open' AND status IN ('open', 'reopen')
        """)
        skill_rows = cursor.fetchall()
        all_skills = set()
        for row in skill_rows:
            for field in ['required_skills', 'main_subjects', 'minor_subjects']:
                if row[field]:
                    skills = [s.strip().lower() for s in row[field].split(',')]
                    all_skills.update(skills)
        all_skills = sorted(list(all_skills))

        search_type = request.form.get('search_type')
        search_query = request.form.get('search_query', '').strip().lower()
        selected_skills = request.form.getlist('selected_skills')

        # Sanitize selected_skills
        selected_skills = [skill.strip().lower() for skill in selected_skills if skill.strip()]

        internships = []
        if has_qualification:
            if search_type == 'skills' and selected_skills:
                # Use LIKE for partial matches
                match_count_sql_parts = []
                condition_sql_parts = []
                params = []

                for skill in selected_skills:
                    pattern = f"%{skill}%"
                    match_count_sql_parts.extend([
                        f"IF(LOWER(i.required_skills) LIKE %s, 1, 0)",
                        f"IF(LOWER(i.main_subjects) LIKE %s, 1, 0)",
                        f"IF(LOWER(i.minor_subjects) LIKE %s, 1, 0)"
                    ])
                    condition_sql_parts.extend([
                        "LOWER(i.required_skills) LIKE %s",
                        "LOWER(i.main_subjects) LIKE %s",
                        "LOWER(i.minor_subjects) LIKE %s"
                    ])
                    params.extend([pattern, pattern, pattern])

                match_count_sql = ' + '.join(match_count_sql_parts)
                conditions = ' OR '.join(condition_sql_parts)

                query = f"""
                    SELECT 
                        i.*, 
                        c.company_name, 
                        c.website_url,
                        ({match_count_sql}) AS match_count
                    FROM internship i
                    JOIN company c ON i.company_id = c.company_id
                    WHERE i.internship_status = 'open' AND i.status IN ('open', 'reopen')
                    AND ({conditions})
                    ORDER BY match_count DESC, i.title ASC
                """
                cursor.execute(query, params + params)  # Double params for match_count and WHERE
                internships = cursor.fetchall()

            elif search_type == 'company' and search_query:
                pattern = f"%{search_query}%"
                cursor.execute("""
                    SELECT i.*, c.company_name, c.website_url
                    FROM internship i
                    JOIN company c ON i.company_id = c.company_id
                    WHERE i.internship_status = 'open' AND i.status IN ('open', 'reopen')
                    AND LOWER(c.company_name) LIKE %s
                    ORDER BY i.title ASC
                """, (pattern,))
                internships = cursor.fetchall()

            elif search_type == 'job_role' and search_query:
                pattern = f"%{search_query}%"
                cursor.execute("""
                    SELECT i.*, c.company_name, c.website_url
                    FROM internship i
                    JOIN company c ON i.company_id = c.company_id
                    WHERE i.internship_status = 'open' AND i.status IN ('open', 'reopen')
                    AND LOWER(i.title) LIKE %s
                    ORDER BY i.title ASC
                """, (pattern,))
                internships = cursor.fetchall()

            else:
                # Default: fetch all open internships
                cursor.execute("""
                    SELECT i.*, c.company_name, c.website_url
                    FROM internship i
                    JOIN company c ON i.company_id = c.company_id
                    WHERE i.internship_status = 'open' AND i.status IN ('open', 'reopen')
                    ORDER BY i.title ASC
                """)
                internships = cursor.fetchall()

        # Add application status
        for internship in internships:
            cursor.execute("""
                SELECT status FROM applications
                WHERE user_id = %s AND internship_id = %s
                ORDER BY applied_on DESC LIMIT 1
            """, (user_id, internship['internship_id']))
            application = cursor.fetchone()
            internship['applied'] = bool(application)
            internship['application_status'] = application['status'] if application else None

        return render_template('applicant_dashboard.html',
                               applicant_name=applicant_name,
                               has_qualification=has_qualification,
                               internships=internships,
                               search_performed=bool(search_type),
                               search_query=search_query,
                               search_type=search_type,
                               all_skills=all_skills,
                               selected_skills=selected_skills)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('applicant_dashboard.html',
                               applicant_name='Unknown User',
                               has_qualification=False,
                               internships=[],
                               all_skills=[],
                               selected_skills=[],
                               error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('applicant_dashboard.html',
                               applicant_name='Unknown User',
                               has_qualification=False,
                               internships=[],
                               all_skills=[],
                               selected_skills=[],
                               error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()            
            
            

@app.route('/apply/<int:internship_id>', methods=['POST'])
def apply_internship(internship_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch internship details
    cursor.execute("""
        SELECT title, required_skills, main_subjects, minor_subjects, open_date
        FROM internship
        WHERE internship_id = %s
    """, (internship_id,))
    internship = cursor.fetchone()

    if not internship:
        cursor.close()
        conn.close()
        return redirect(url_for('applicant_dashboard', msg='Internship not found.'))

    # Check if internship is open
    open_date = internship['open_date']
    if isinstance(open_date, datetime):
        open_date = open_date.date()

    if open_date > date.today():
        msg = f"You can apply after the internship opens on {open_date.strftime('%Y-%m-%d')}"
        cursor.close()
        conn.close()
        return redirect(url_for('applicant_dashboard', msg=msg))
    


    # Fetch applicant's qualifications
    applicant_skills, applicant_main_subjects, applicant_sub_subjects = fetch_and_combine_applicant_qualifications(user_id, cursor)

    # Calculate skill match percentage
    skill_match_percentage = calculate_skill_match_percentage(
        internship['required_skills'],
        internship['main_subjects'],
        internship['minor_subjects'],
        applicant_skills,
        applicant_main_subjects,
        applicant_sub_subjects
    )

    # Check for existing application
    cursor.execute("""
        SELECT status FROM applications
        WHERE user_id = %s AND internship_id = %s
    """, (user_id, internship_id))
    existing_application = cursor.fetchone()

    if existing_application:
        if existing_application['status'] in ['Withdrawn', 'Rejected']:
            cursor.execute("""
                INSERT INTO applications (user_id, internship_id, applied_on, status, skill_match_percentage)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, internship_id, date.today(), 'Pending', skill_match_percentage))
        else:
            cursor.close()
            conn.close()
            return redirect(url_for('applicant_dashboard', msg='You have already applied for this internship.'))
    else:
        cursor.execute("""
            INSERT INTO applications (user_id, internship_id, applied_on, status, skill_match_percentage)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, internship_id, date.today(), 'Pending', skill_match_percentage))

    # ✅ Fetch applicant email and name
    cursor.execute("""
        SELECT fname, lname, email FROM applicant WHERE user_id = %s
    """, (user_id,))
    applicant = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    # ✅ Send confirmation email to applicant
    subject = "Xtern: Internship Application Submitted"
    content = f"""
Dear {applicant['fname']} {applicant['lname']},

You have successfully applied to the internship position: <b>{internship['title']}</b> on <b>Xtern</b>.

Our team and the company will review your application shortly. You can track your application status from your dashboard.

Best of luck!

Best regards,<br>
Xtern Team
"""
    send_email(
        to=applicant['email'],
        subject=subject,
        content=content,
        is_html=True
    )

    return redirect(url_for('applicant_dashboard', msg='Successfully applied to the internship!'))




@app.route('/my_applications')
def my_applications():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.application_id, a.status,
               i.title AS internship_title, i.description AS internship_description,
               i.stipend, i.duration, i.location,
               c.company_name, c.website_url
        FROM applications a
        JOIN internship i ON a.internship_id = i.internship_id
        JOIN company c ON i.company_id = c.company_id
        WHERE a.user_id = %s
    """, (user_id,))
    user_applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('my_applications.html', user_applications=user_applications)




@app.route('/withdraw_application/<int:application_id>', methods=['POST'])
def withdraw_application(application_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the application exists and belongs to the current user
    cursor.execute("""
        SELECT a.application_id, a.status, i.title, ap.fname, ap.lname, ap.email
        FROM applications a
        JOIN internship i ON a.internship_id = i.internship_id
        JOIN applicant ap ON a.user_id = ap.user_id
        WHERE a.application_id = %s AND a.user_id = %s
    """, (application_id, user_id))
    
    application = cursor.fetchone()

    if application and application['status'] == 'Pending':
        # Update the application status to withdrawn
        cursor.execute("UPDATE applications SET status = 'Withdrawn' WHERE application_id = %s", (application_id,))
        conn.commit()

        # ✅ Send email to applicant
        subject = "Xtern: Internship Application Withdrawn"
        content = f"""
Dear {application['fname']} {application['lname']},

You have successfully withdrawn your application for the internship: <b>{application['title']}</b>.

If this was a mistake, you may reapply later if the application window is still open.

Thank you for using <b>Xtern</b>.

Best regards,<br>
Xtern Team
"""
        send_email(
            to=application['email'],
            subject=subject,
            content=content,
            is_html=True
        )

        msg = "Your application has been successfully withdrawn."
    else:
        msg = "You cannot withdraw this application or it does not exist."

    cursor.close()
    conn.close()

    return redirect(url_for('my_applications', msg=msg))




@app.route('/applicant/add_qualification', methods=['GET', 'POST'])
def add_qualification():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

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
    if not user_id:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('applicant_login'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch applicant name
        cursor.execute("SELECT CONCAT(fname, ' ', lname) AS name FROM applicant WHERE user_id = %s", (user_id,))
        applicant = cursor.fetchone()
        applicant_name = applicant['name'] if applicant else 'Unknown User'

        # Fetch qualifications
        query = """
            SELECT uq.*, d.degree_name 
            FROM user_qualification uq
            JOIN degree d ON uq.degree_id = d.degree_id
            WHERE uq.user_id = %s
        """
        cursor.execute(query, (user_id,))
        qualifications = cursor.fetchall()

        return render_template('applicant_myqualifications.html',
                               qualifications=qualifications,
                               applicant_name=applicant_name)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('applicant_myqualifications.html',
                               qualifications=[],
                               applicant_name='Unknown User',
                               error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('applicant_myqualifications.html',
                               qualifications=[],
                               applicant_name='Unknown User',
                               error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



@app.route('/applicant/update_qualification', methods=['GET', 'POST'])
def update_qualification():
    user_id = session.get('user_id')
    if not user_id:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('applicant_login'))

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        qualification_id = request.args.get('qualification_id')

        if request.method == 'POST':
            # Get form data
            degree_id = request.form['degree_id']
            year = request.form['year']
            board = request.form['board']
            percentage = request.form['percentage']
            main_subjects = request.form['main_subjects']
            sub_subjects = request.form['sub_subjects']
            skills = request.form['skills']
            interest = request.form['interest']
            institute = request.form['institute']

            # Update query
            cursor.execute("""
                UPDATE user_qualification
                SET degree_id=%s, year=%s, board=%s, percentage=%s, main_subjects=%s, 
                    sub_subjects=%s, skills=%s, interest=%s, institute=%s
                WHERE qualification_id=%s AND user_id=%s
            """, (degree_id, year, board, percentage, main_subjects, sub_subjects, skills, interest, institute, qualification_id, user_id))

            conn.commit()
            return redirect(url_for('applicant_myqualifications', msg="Qualification updated successfully"))

        # GET request: prefill form with existing data
        cursor.execute("""
            SELECT * FROM user_qualification 
            WHERE qualification_id = %s AND user_id = %s
        """, (qualification_id, user_id))
        qualification = cursor.fetchone()

        if not qualification:
            return redirect(url_for('applicant_myqualifications', error="Qualification not found"))

        cursor.execute("SELECT * FROM degree")
        degrees = cursor.fetchall()

        return render_template("update_qualification.html",
                               qualification=qualification,
                               degrees=degrees)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template("update_qualification.html",
                               qualification=None,
                               degrees=[],
                               error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template("update_qualification.html",
                               qualification=None,
                               degrees=[],
                               error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()






@app.route('/applicant/profile', methods=['GET', 'POST'])
def applicant_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Get updated form data
            fname = request.form.get('fname')
            lname = request.form.get('lname')
            phone = request.form.get('phone')
            city = request.form.get('city')
            state = request.form.get('state')
            resume_file = request.files.get('resume')

            # Fetch current applicant data for email and old resume
            cursor.execute("SELECT email, resume_url FROM applicant WHERE user_id = %s", (user_id,))
            applicant = cursor.fetchone()
            if not applicant:
                return render_template('applicant_profile.html', error="Applicant not found."), 404

            resume_url = applicant['resume_url']  # Current resume path
            update_params = [fname, lname, phone, city, state, user_id]

            # Handle resume upload
            if resume_file and resume_file.filename != '':
                filename = secure_filename(resume_file.filename)
                extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

                if extension not in ALLOWED_EXTENSIONS:
                    return render_template('applicant_profile.html', applicant=applicant, error="Resume must be a PDF, DOC, or DOCX file.")

                # Generate new filename using email
                new_filename = f"{applicant['email'].replace('@', '_').replace('.', '_')}.{extension}"
                resume_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename).replace('/', '\\')  # Windows-style path
                resume_file.save(resume_path)

                # Delete old resume if it exists
                if resume_url and os.path.exists(resume_url):
                    try:
                        os.remove(resume_url)
                    except OSError:
                        pass  # Ignore deletion errors

                resume_url = resume_path
                update_query = """
                    UPDATE applicant 
                    SET fname = %s, lname = %s, contact_no = %s, city = %s, state = %s, resume_url = %s
                    WHERE user_id = %s
                """
                update_params = [fname, lname, phone, city, state, resume_url, user_id]
            else:
                update_query = """
                    UPDATE applicant 
                    SET fname = %s, lname = %s, contact_no = %s, city = %s, state = %s
                    WHERE user_id = %s
                """

            # Update database
            cursor.execute(update_query, update_params)
            conn.commit()

            return redirect(url_for("applicant_dashboard"))

        # Fetch latest profile info
        cursor.execute("SELECT * FROM applicant WHERE user_id = %s", (user_id,))
        applicant = cursor.fetchone()

        if not applicant:
            return render_template('applicant_profile.html', error="Applicant not found."), 404

        return render_template('applicant_profile.html', applicant=applicant)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('applicant_profile.html', applicant=applicant, error=f"Database error: {err}"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
            
            
@app.route('/applicant/feedback', methods=['GET', 'POST'])
def applicant_feedback():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True,buffered=True)

        # Fetch companies the intern applied to
        cursor.execute("""
            SELECT DISTINCT c.company_id, c.company_name
            FROM company c
            JOIN internship i ON c.company_id = i.company_id
            JOIN applications app ON i.internship_id = app.internship_id
            WHERE app.user_id = %s
        """, (user_id,))
        companies = cursor.fetchall()

        # Fetch feedback given by companies to the intern
        cursor.execute("""
            SELECT f.feedback_id, f.feedback_text, f.rating, f.date_given, c.company_name
            FROM feedback f
            JOIN company c ON f.company_id = c.company_id
            WHERE f.user_id = %s AND f.given_by = 'company'
            ORDER BY f.date_given DESC
        """, (user_id,))
        received_feedback = cursor.fetchall()

        # Get intern email and name
        cursor.execute("SELECT email, fname, lname FROM applicant WHERE user_id = %s", (user_id,))
        intern = cursor.fetchone()
        intern_email = intern['email']
        intern_name = f"{intern['fname']} {intern['lname']}"

        if request.method == 'POST':
            feedback_type = request.form.get('feedback_type')
            feedback_text = request.form.get('feedback_text')
            rating = request.form.get('rating')
            company_id = request.form.get('company_id') if feedback_type == 'company' else None

            # Validate inputs
            if not feedback_text:
                return render_template('applicant_feedback.html', error="Feedback text is required.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400
            if not feedback_type or feedback_type not in ['xtern', 'company']:
                return render_template('applicant_feedback.html', error="Invalid feedback type.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400
            if feedback_type == 'company' and not company_id:
                return render_template('applicant_feedback.html', error="Please select a company.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400

            # Validate rating
            try:
                rating_int = int(rating)
                if rating_int < 1 or rating_int > 5:
                    return render_template('applicant_feedback.html', error="Rating must be between 1 and 5.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400
            except (ValueError, TypeError):
                return render_template('applicant_feedback.html', error="Invalid rating format.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400

            # Validate company_id for company feedback
            if feedback_type == 'company':
                cursor.execute("""
                    SELECT *
                    FROM applications app
                    JOIN internship i ON app.internship_id = i.internship_id
                    WHERE app.user_id = %s AND i.company_id = %s
                """, (user_id, company_id))
                if not cursor.fetchone():
                    return render_template('applicant_feedback.html', error="Selected company is not associated with your applications.", companies=companies, received_feedback=received_feedback, applicant_name=intern_name), 400

                # Get company email and name
                cursor.execute("SELECT email, company_name FROM company WHERE company_id = %s", (company_id,))
                company = cursor.fetchone()
                company_email = company['email']
                company_name = company['company_name']

            # Insert feedback
            cursor.execute("""
                INSERT INTO feedback (user_id, company_id, given_by, feedback_text, rating, date_given)
                VALUES (%s, %s, 'applicant', %s, %s, NOW())
            """, (user_id, company_id, feedback_text, rating_int))
            conn.commit()

            # Email to Intern
            subject_intern = f"✅ Feedback Submitted: {feedback_type.capitalize()} Feedback"
            content_intern = f"""
Hello {intern_name},

Thank you for submitting your feedback on the {feedback_type}.

📌 **Feedback Details**:
- Type: {feedback_type.capitalize()}
- Rating: {rating_int}/5
- Feedback Text: {feedback_text}
- Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}

This confirmation ensures your feedback has been securely recorded.

Warm regards,  
Xtern Internship Portal
"""
            send_email(to=intern_email, subject=subject_intern, content=content_intern, is_html=False)

            # Email to Company (if applicable)
            if feedback_type == 'company':
                subject_company = f"📢 Feedback Received from {intern_name}"
                content_company = f"""
Hello {company_name},

You have received new feedback from **{intern_name}** regarding your internship opportunity.

📌 **Feedback Details**:
- Rating: {rating_int}/5
- Feedback Text: {feedback_text}
- Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}

Thank you for your participation in the Xtern Internship Portal.

Warm regards,  
Xtern Internship Portal
"""
                send_email(to=company_email, subject=subject_company, content=content_company, is_html=False)

            return redirect(url_for('applicant_dashboard'))

        return render_template('applicant_feedback.html', companies=companies, received_feedback=received_feedback, error=None, applicant_name=intern_name)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('applicant_feedback.html', error=f"Database error: {err}", companies=[], received_feedback=[], applicant_name=intern_name), 500
    except Exception as e:
        print(f"An unexpected error: {e}")
        return render_template('applicant_feedback.html', error=f"An unexpected error occurred: {e}", companies=[], received_feedback=[], applicant_name=intern_name), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
                        



# Assuming get_db_connection is defined elsewhere
# from . import get_db_connection

@app.route('/applicant/analytics')
def applicant_analytics():
    # Check if user is logged in
    if 'user_id' not in session:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('applicant_login'))

    user_id = session['user_id']
    conn = None
    cursor = None

    # Initialize all template variables to avoid undefined errors
    applicant_name = 'Unknown User'
    total_applied = 0
    approved = 0
    rejected = 0
    pending = 0
    skills_matched = 0
    avg_skill_match = 0.0
    applications_per_category = []
    status_distribution = {'labels': ['Approved', 'Rejected', 'Pending'], 'data': [0, 0, 0]}
    category_labels = []
    category_data = []
    monthly_labels = []
    monthly_data = []
    skill_match_labels = []
    skill_match_percentages = []
    top_skills = []
    user_skill_counts = []
    required_skill_counts = []
    approval_rate_labels = []
    approval_rate_data = []
    outcome_labels = []
    outcome_approved = []
    outcome_rejected = []

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)  # Add buffered=True

        # Fetch applicant name
        cursor.execute("SELECT CONCAT(fname, ' ', lname) AS name FROM applicant WHERE user_id = %s", (user_id,))
        applicant = cursor.fetchone()
        applicant_name = applicant['name'] if applicant else 'Unknown User'

        # Numerical Analytics
        # 1. Total Internships Applied
        cursor.execute("""
            SELECT COUNT(*) AS total_applied
            FROM applications
            WHERE user_id = %s
        """, (user_id,))
        total_applied = cursor.fetchone()['total_applied']

        # 2. Applications Approved
        cursor.execute("""
            SELECT COUNT(*) AS approved
            FROM applications
            WHERE user_id = %s AND status = 'Approved'
        """, (user_id,))
        approved = cursor.fetchone()['approved']

        # 3. Applications Rejected
        cursor.execute("""
            SELECT COUNT(*) AS rejected
            FROM applications
            WHERE user_id = %s AND status = 'Rejected'
        """, (user_id,))
        rejected = cursor.fetchone()['rejected']

        # 4. Applications Pending
        cursor.execute("""
            SELECT COUNT(*) AS pending
            FROM applications
            WHERE user_id = %s AND status = 'Pending'
        """, (user_id,))
        pending = cursor.fetchone()['pending']

        # 5. Skills Matched in Applications (Count)
        cursor.execute("""
            SELECT COUNT(*) AS skills_matched
            FROM applications
            WHERE user_id = %s AND skill_match_percentage > 0
        """, (user_id,))
        skills_matched = cursor.fetchone()['skills_matched']

        # 6. Internships Applied Per Category/Field
        cursor.execute("""
            SELECT i.title AS category, COUNT(a.application_id) AS count
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE a.user_id = %s
            GROUP BY i.title
        """, (user_id,))
        applications_per_category = cursor.fetchall()
        category_labels = [row['category'] for row in applications_per_category]
        category_data = [row['count'] for row in applications_per_category]

        # 7. Avg. Skill Match Percentage Across All Applications
        cursor.execute("""
            SELECT AVG(skill_match_percentage) AS avg_skill_match
            FROM applications
            WHERE user_id = %s AND skill_match_percentage IS NOT NULL
        """, (user_id,))
        avg_result = cursor.fetchone()
        avg_skill_match = round(avg_result['avg_skill_match'], 2) if avg_result['avg_skill_match'] else 0.0

        # Graphical Analytics Data
        # 1. Application Status Distribution
        status_distribution = {
            'labels': ['Approved', 'Rejected', 'Pending'],
            'data': [approved, rejected, pending]
        }

        # 2. Monthly Applications Timeline
        cursor.execute("""
            SELECT DATE_FORMAT(applied_on, '%Y-%m') AS month, COUNT(*) AS count
            FROM applications
            WHERE user_id = %s
            GROUP BY YEAR(applied_on), MONTH(applied_on)
            ORDER BY YEAR(applied_on), MONTH(applied_on)
        """, (user_id,))
        monthly_applications = cursor.fetchall()
        monthly_labels = [row['month'] for row in monthly_applications]
        monthly_data = [row['count'] for row in monthly_applications]

        # 3. Skill Match % Per Internship
        cursor.execute("""
            SELECT i.title, a.skill_match_percentage
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE a.user_id = %s AND a.skill_match_percentage IS NOT NULL
        """, (user_id,))
        skill_match_data = cursor.fetchall()
        skill_match_labels = [row['title'] for row in skill_match_data]
        skill_match_percentages = [row['skill_match_percentage'] for row in skill_match_data]

        # 4. Top Skills Required vs Your Skills
        cursor.execute("""
            SELECT required_skills
            FROM internship i
            JOIN applications a ON i.internship_id = a.internship_id
            WHERE a.user_id = %s
        """, (user_id,))
        required_skills_rows = cursor.fetchall()
        required_skills = set()
        for row in required_skills_rows:
            if row['required_skills']:
                skills = [skill.strip() for skill in row['required_skills'].split(',') if skill.strip()]
                required_skills.update(skills)

        cursor.execute("""
            SELECT skills
            FROM user_qualification
            WHERE user_id = %s
        """, (user_id,))
        user_skills_rows = cursor.fetchall()  # Handle multiple qualifications
        user_skills = set()
        for row in user_skills_rows:
            if row['skills']:
                skills = [skill.strip() for skill in row['skills'].split(',') if skill.strip()]
                user_skills.update(skills)

        top_skills = list(required_skills)[:5]  # Limit to top 5
        user_skill_counts = [1 if skill in user_skills else 0 for skill in top_skills]
        required_skill_counts = [1 for _ in top_skills]

        # 5. Approval Rate Trend
        cursor.execute("""
            SELECT DATE_FORMAT(applied_on, '%Y-%m') AS month,
                   SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) / COUNT(*) AS approval_rate
            FROM applications
            WHERE user_id = %s
            GROUP BY YEAR(applied_on), MONTH(applied_on)
            ORDER BY YEAR(applied_on), MONTH(applied_on)
        """, (user_id,))
        approval_rate_data_rows = cursor.fetchall()
        approval_rate_labels = [row['month'] for row in approval_rate_data_rows]
        approval_rate_data = [round(row['approval_rate'] * 100, 2) for row in approval_rate_data_rows]

        # 6. Application Outcome Timeline
        cursor.execute("""
            SELECT DATE_FORMAT(applied_on, '%Y-%m') AS month,
                   SUM(CASE WHEN status = 'Approved' THEN 1 ELSE 0 END) AS approved,
                   SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END) AS rejected
            FROM applications
            WHERE user_id = %s
            GROUP BY YEAR(applied_on), MONTH(applied_on)
            ORDER BY YEAR(applied_on), MONTH(applied_on)
        """, (user_id,))
        outcome_data = cursor.fetchall()
        outcome_labels = [row['month'] for row in outcome_data]
        outcome_approved = [row['approved'] for row in outcome_data]
        outcome_rejected = [row['rejected'] for row in outcome_data]

        return render_template(
            'applicant_analytics.html',
            applicant_name=applicant_name,
            total_applied=total_applied,
            approved=approved,
            rejected=rejected,
            pending=pending,
            skills_matched=skills_matched,
            avg_skill_match=avg_skill_match,
            applications_per_category=applications_per_category,
            status_distribution=status_distribution,
            category_labels=category_labels,
            category_data=category_data,
            monthly_labels=monthly_labels,
            monthly_data=monthly_data,
            skill_match_labels=skill_match_labels,
            skill_match_percentages=skill_match_percentages,
            top_skills=top_skills,
            user_skill_counts=user_skill_counts,
            required_skill_counts=required_skill_counts,
            approval_rate_labels=approval_rate_labels,
            approval_rate_data=approval_rate_data,
            outcome_labels=outcome_labels,
            outcome_approved=outcome_approved,
            outcome_rejected=outcome_rejected
        )

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template(
            'applicant_analytics.html',
            applicant_name=applicant_name,
            total_applied=total_applied,
            approved=approved,
            rejected=rejected,
            pending=pending,
            skills_matched=skills_matched,
            avg_skill_match=avg_skill_match,
            applications_per_category=applications_per_category,
            status_distribution=status_distribution,
            category_labels=category_labels,
            category_data=category_data,
            monthly_labels=monthly_labels,
            monthly_data=monthly_data,
            skill_match_labels=skill_match_labels,
            skill_match_percentages=skill_match_percentages,
            top_skills=top_skills,
            user_skill_counts=user_skill_counts,
            required_skill_counts=required_skill_counts,
            approval_rate_labels=approval_rate_labels,
            approval_rate_data=approval_rate_data,
            outcome_labels=outcome_labels,
            outcome_approved=outcome_approved,
            outcome_rejected=outcome_rejected,
            error=f"Database error: {err}"
        ), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template(
            'applicant_analytics.html',
            applicant_name=applicant_name,
            total_applied=total_applied,
            approved=approved,
            rejected=rejected,
            pending=pending,
            skills_matched=skills_matched,
            avg_skill_match=avg_skill_match,
            applications_per_category=applications_per_category,
            status_distribution=status_distribution,
            category_labels=category_labels,
            category_data=category_data,
            monthly_labels=monthly_labels,
            monthly_data=monthly_data,
            skill_match_labels=skill_match_labels,
            skill_match_percentages=skill_match_percentages,
            top_skills=top_skills,
            user_skill_counts=user_skill_counts,
            required_skill_counts=required_skill_counts,
            approval_rate_labels=approval_rate_labels,
            approval_rate_data=approval_rate_data,
            outcome_labels=outcome_labels,
            outcome_approved=outcome_approved,
            outcome_rejected=outcome_rejected,
            error=f"An unexpected error occurred: {e}"
        ), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except:
                pass



@app.context_processor
def inject_applicant_name():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT fname, lname FROM applicant WHERE user_id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            full_name = f"{user['fname']} {user['lname']}"
            return dict(applicant_name=full_name)
    return dict(applicant_name="Applicant")


@app.context_processor
def inject_company_name():
    company_id = session.get('company_id')  # Assuming you store this in session
    if company_id:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT company_name FROM company WHERE company_id = %s", (company_id,))
        company = cursor.fetchone()
        cursor.close()
        conn.close()
        if company:
            return dict(company_name=company['company_name'])
    return dict(company_name="Company")



@app.route('/company/dashboard')
def company_dashboard():
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch company name
        cursor.execute("SELECT company_name FROM company WHERE company_id = %s", (company_id,))
        company = cursor.fetchone()
        company_name = company['company_name'] if company else 'Unknown Company'

        # Fetch internships with applicant count and days left
        cursor.execute("""
            SELECT i.*, 
                   (DATEDIFF(i.close_date, CURDATE())) AS days_left,
                   (SELECT COUNT(*) FROM applications a WHERE a.internship_id = i.internship_id) AS applicant_count
            FROM internship i
            WHERE i.company_id = %s
            ORDER BY i.open_date DESC
        """, (company_id,))
        internships = cursor.fetchall()

        return render_template('company_dashboard.html', internships=internships, company_name=company_name)

    except mysql.connector.Error as err:
        return render_template('company_dashboard.html', internships=[], company_name='Unknown Company', error=f"Database error: {err}"), 500
    except Exception as e:
        return render_template('company_dashboard.html', internships=[], company_name='Unknown Company', error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

@app.route('/company/applications')
def company_applications():
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    internship_id = request.args.get('internship_id', type=int)
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch company name
        cursor.execute("SELECT company_name FROM company WHERE company_id = %s", (company_id,))
        company = cursor.fetchone()
        company_name = company['company_name'] if company else 'Unknown Company'

        # Base query for applications
        query = """
            SELECT 
                a.application_id, a.status AS application_status, a.skill_match_percentage, a.remarks, a.applied_on,
                u.user_id, u.fname AS applicant_name, u.email, u.contact_no, u.city, u.state, u.resume_url,
                i.internship_id, i.title AS internship_title, i.post, i.location, 
                i.description AS internship_description, i.stipend, i.duration,
                c.company_name, c.website_url
            FROM applications a
            JOIN applicant u ON a.user_id = u.user_id
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN company c ON i.company_id = c.company_id
            WHERE i.company_id = %s
        """
        params = [company_id]

        # Add internship_id filter if provided
        if internship_id:
            query += " AND a.internship_id = %s"
            params.append(internship_id)

        query += " ORDER BY a.skill_match_percentage DESC, a.application_id DESC"
        cursor.execute(query, params)
        applications = cursor.fetchall()

        # Process resume filenames
        for app in applications:
            if app['resume_url']:
                normalized_path = app['resume_url'].replace('\\', '/')
                app['resume_filename'] = os.path.basename(normalized_path)
            else:
                app['resume_filename'] = None

        return render_template('company_applications.html', applications=applications, company_name=company_name)

    except mysql.connector.Error as err:
        return render_template('company_applications.html', applications=[], company_name='Unknown Company', error=f"Database error: {err}"), 500
    except Exception as e:
        return render_template('company_applications.html', applications=[], company_name='Unknown Company', error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()



@app.route('/download_resume/<filename>')
def download_resume(filename):
    resume_folder = os.path.join(app.root_path, 'static', 'resumes')
    full_path = os.path.join(resume_folder, filename)
    print(f"Trying to serve: {full_path}")

    if not os.path.exists(full_path):
        return "Resume not found", 404

    return send_from_directory(resume_folder, filename, as_attachment=True)





@app.route('/company/approve_application/<int:application_id>', methods=['POST'])
def approve_application(application_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch details for the email
    cursor.execute("""
        SELECT a.application_id, ap.email, ap.fname, ap.lname, i.title, c.company_name AS company_name
        FROM applications a
        JOIN applicant ap ON a.user_id = ap.user_id
        JOIN internship i ON a.internship_id = i.internship_id
        JOIN company c ON i.company_id = c.company_id
        WHERE a.application_id = %s AND c.company_id = %s
    """, (application_id, company_id))
    
    application_info = cursor.fetchone()

    if application_info:
        # Update status
        cursor.execute("UPDATE applications SET status = 'Approved' WHERE application_id = %s", (application_id,))
        conn.commit()

        # ✅ Send email to applicant
        subject = f"Congratulations! Your Application is Approved by {application_info['company_name']}"
        content = f"""
Dear {application_info['fname']} {application_info['lname']},

We are pleased to inform you that your application for the internship titled <b>{application_info['title']}</b> has been <b>approved</b> by <b>{application_info['company_name']}</b>.

You will be contacted shortly with further steps and onboarding details.

Congratulations once again, and we look forward to seeing your contributions!

Best regards,<br>
{application_info['company_name']}<br>
Xtern Platform
"""
        send_email(
            to=application_info['email'],
            subject=subject,
            content=content,
            is_html=True
        )

    cursor.close()
    conn.close()
    return redirect(url_for('company_applications'))



@app.route('/company/reject_application/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch details to send rejection email
    cursor.execute("""
        SELECT a.application_id, ap.email, ap.fname, ap.lname, i.title, c.company_name AS company_name
        FROM applications a
        JOIN applicant ap ON a.user_id = ap.user_id
        JOIN internship i ON a.internship_id = i.internship_id
        JOIN company c ON i.company_id = c.company_id
        WHERE a.application_id = %s AND c.company_id = %s
    """, (application_id, company_id))

    application_info = cursor.fetchone()

    if application_info:
        # Update application status to 'Rejected'
        cursor.execute("UPDATE applications SET status = 'Rejected' WHERE application_id = %s", (application_id,))
        conn.commit()

        # ✅ Send rejection email to the intern
        subject = f"Application Update from {application_info['company_name']}"
        content = f"""
Dear {application_info['fname']} {application_info['lname']},

Thank you for applying for the internship titled <b>{application_info['title']}</b> at <b>{application_info['company_name']}</b>.

We appreciate your interest and the time you took to apply. However, after careful consideration, we regret to inform you that your application has not been selected for this position.

We encourage you to continue applying to other opportunities on our platform that match your skills and interests.

Wishing you all the best in your career journey.

Warm regards,<br>
{application_info['company_name']}<br>
Xtern Platform
"""
        send_email(
            to=application_info['email'],
            subject=subject,
            content=content,
            is_html=True
        )

    cursor.close()
    conn.close()
    return redirect(url_for('company_applications'))



@app.route('/company/analytics')
def company_analytics():
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Debug: Print company_id
        print("company_id:", company_id, "type:", type(company_id))

        # Fetch company details for sidebar
        print("Executing: Fetch company details")
        cursor.execute("SELECT company_name, industry FROM company WHERE company_id = %s", (company_id,))
        company_data = cursor.fetchone()
        company_name = company_data[0] if company_data else "Unknown Company"
        company_industry = company_data[1] if company_data else "Unknown Industry"

        # Total internships
        print("Executing: Total internships")
        cursor.execute("SELECT COUNT(*) FROM internship WHERE company_id = %s", (company_id,))
        total_internships = cursor.fetchone()[0]

        # Active internships
        print("Executing: Active internships")
        cursor.execute("SELECT COUNT(*) FROM internship WHERE company_id = %s AND status = 'Open'", (company_id,))
        active_internships = cursor.fetchone()[0]

        # Total applications
        print("Executing: Total applications")
        cursor.execute("""
            SELECT COUNT(*)
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s
        """, (company_id,))
        total_applications = cursor.fetchone()[0]

        # Approved applications
        print("Executing: Approved applications")
        cursor.execute("""
            SELECT COUNT(*)
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s AND a.status = 'Approved'
        """, (company_id,))
        approved_applications = cursor.fetchone()[0]

        # Rejected applications
        print("Executing: Rejected applications")
        cursor.execute("""
            SELECT COUNT(*)
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s AND a.status = 'Rejected'
        """, (company_id,))
        rejected_applications = cursor.fetchone()[0]

        # Pending applications
        print("Executing: Pending applications")
        cursor.execute("""
            SELECT COUNT(*)
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s AND a.status = 'Pending'
        """, (company_id,))
        pending_applications = cursor.fetchone()[0]

        # Average skill match percentage
        print("Executing: Average skill match")
        cursor.execute("""
            SELECT ROUND(AVG(a.skill_match_percentage), 2)
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s
        """, (company_id,))
        avg_skill_match = cursor.fetchone()[0] or 0.0  # Default to 0.0 if no applications

        # Most applied internship
        print("Executing: Most applied internship")
        cursor.execute("""
            SELECT i.title
            FROM internship i
            LEFT JOIN applications a ON i.internship_id = a.internship_id
            WHERE i.company_id = %s
            GROUP BY i.internship_id, i.title
            ORDER BY COUNT(a.application_id) DESC
            LIMIT 1
        """, (company_id,))
        most_applied_internship = cursor.fetchone()
        most_applied_internship = most_applied_internship[0] if most_applied_internship else "None"

        # Application status breakdown
        print("Executing: Application status breakdown")
        cursor.execute("""
            SELECT a.status, COUNT(*) 
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s
            GROUP BY a.status
        """, (company_id,))
        status_rows = cursor.fetchall()
        application_status = {status: count for status, count in status_rows}

        # Skill match distribution
        skill_match = {
            "90-100%": 0,
            "75-89%": 0,
            "50-74%": 0,
            "0-49%": 0
        }
        print("Executing: Skill match distribution")
        cursor.execute("""
            SELECT a.skill_match_percentage
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s
        """, (company_id,))
        for (match,) in cursor.fetchall():
            if match is not None:
                if match >= 90:
                    skill_match["90-100%"] += 1
                elif match >= 75:
                    skill_match["75-89%"] += 1
                elif match >= 50:
                    skill_match["50-74%"] += 1
                else:
                    skill_match["0-49%"] += 1

        # Applications Per Internship
        print("Executing: Applications per internship")
        cursor.execute("""
            SELECT i.title, COUNT(a.application_id) AS application_count
            FROM internship i
            LEFT JOIN applications a ON i.internship_id = a.internship_id
            WHERE i.company_id = %s
            GROUP BY i.internship_id, i.title
        """, (company_id,))
        applications_per_internship = [{"title": title, "count": count} for title, count in cursor.fetchall()]

        # Monthly Applications Trend
        print("Executing: Monthly applications trend")
        cursor.execute("""
            SELECT DATE_FORMAT(a.applied_on, '%b-%Y') AS month_year, COUNT(*) AS count
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            WHERE i.company_id = %s
            GROUP BY YEAR(a.applied_on), MONTH(a.applied_on)
            ORDER BY YEAR(a.applied_on), MONTH(a.applied_on)
        """, (company_id,))
        monthly_apps = cursor.fetchall()
        monthly_applications = [{"month": month, "count": count} for month, count in monthly_apps]

        # Degree-wise Applicant Count
        print("Executing: Degree-wise applicant count")
        cursor.execute("""
            SELECT d.degree_name, COUNT(DISTINCT a.user_id) AS applicant_count
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN user_qualification uq ON a.user_id = uq.user_id
            JOIN degree d ON uq.degree_id = d.degree_id
            WHERE i.company_id = %s
            GROUP BY d.degree_id, d.degree_name
        """, (company_id,))
        degree_counts = [{"degree": degree, "count": count} for degree, count in cursor.fetchall()]

        # State-wise Applicants
        print("Executing: State-wise applicants")
        cursor.execute("""
            SELECT ap.state, COUNT(DISTINCT a.user_id) AS applicant_count
            FROM applications a
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN applicant ap ON a.user_id = ap.user_id
            WHERE i.company_id = %s
            GROUP BY ap.state
        """, (company_id,))
        state_counts = [{"state": state, "count": count} for state, count in cursor.fetchall()]

        # Internship performance table
        print("Executing: Internship performance table")
        cursor.execute("""
            SELECT i.internship_id, i.title, i.status,
                   COUNT(a.application_id) AS applications_count,
                   ROUND(AVG(a.skill_match_percentage), 2) AS avg_skill_match
            FROM internship i
            LEFT JOIN applications a ON i.internship_id = a.internship_id
            WHERE i.company_id = %s
            GROUP BY i.internship_id
        """, (company_id,))
        internships = cursor.fetchall()
        internship_stats = []
        for internship in internships:
            internship_stats.append({
                "internship_id": internship[0],
                "title": internship[1],
                "status": internship[2],
                "applications_count": internship[3],
                "avg_skill_match": internship[4] or 0
            })

        stats = {
            "total_internships": total_internships,
            "active_internships": active_internships,
            "total_applications": total_applications,
            "approved_applications": approved_applications,
            "rejected_applications": rejected_applications,
            "pending_applications": pending_applications,
            "avg_skill_match": float(avg_skill_match),
            "most_applied_internship": most_applied_internship
        }

        return render_template('company_analytics.html',
                              stats=stats,
                              application_status=application_status,
                              skill_match=skill_match,
                              applications_per_internship=applications_per_internship,
                              monthly_applications=monthly_applications,
                              degree_counts=degree_counts,
                              state_counts=state_counts,
                              internship_stats=internship_stats,
                              company_name=company_name,
                              company_industry=company_industry)
    finally:
        cursor.close()
        conn.close()


@app.route('/company/internship/<int:internship_id>')
def company_internship_details(internship_id):
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM internship
        WHERE internship_id = %s AND company_id = %s
    """, (internship_id, company_id))

    internship = cursor.fetchone()
    cursor.close()
    conn.close()

    if internship is None:
        return "Internship not found or unauthorized access.", 404

    return render_template('company_internship_details.html', internship=internship)



@app.route('/company/internships')
def view_all_internships():
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM internship
        WHERE company_id = %s
        ORDER BY open_date DESC
    """, (company_id,))
    
    internships = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view_all_internships.html', internships=internships)




@app.route('/company/internship/edit/<int:internship_id>', methods=['GET', 'POST'])
def edit_internship(internship_id):
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if request.method == 'POST':
            # Get updated form data
            title = request.form['title']
            post = request.form['post']
            description = request.form['description']
            duration = request.form['duration']
            required_skills = request.form['required_skills']
            main_subjects = request.form['main_subjects']
            minor_subjects = request.form['minor_subjects']
            stipend = request.form['stipend']
            location = request.form['location']
            remarks = request.form['remarks']
            internship_status = request.form['internship_status']
            open_date = request.form['open_date']
            close_date = request.form['close_date']
            status = request.form['status']
            job_offer = request.form['job_offer']

            # Check if close_date is extended to a future date
            if close_date:
                try:
                    close_date_obj = date.fromisoformat(close_date)
                    if close_date_obj > date.today():
                        internship_status = 'Open'
                        status = 'Open'
                except ValueError:
                    return render_template('edit_internship.html', internship=request.form, error="Invalid close date format."), 400

            # Update internship in database
            cursor.execute("""
                UPDATE internship
                SET title = %s, post = %s, description = %s, duration = %s,
                    required_skills = %s, main_subjects = %s, minor_subjects = %s,
                    stipend = %s, location = %s, remarks = %s,
                    internship_status = %s, open_date = %s, close_date = %s,
                    status = %s, job_offer = %s
                WHERE internship_id = %s AND company_id = %s
            """, (
                title, post, description, duration, required_skills, main_subjects,
                minor_subjects, stipend, location, remarks, internship_status,
                open_date, close_date, status, job_offer, internship_id, company_id
            ))

            if cursor.rowcount == 0:
                raise mysql.connector.Error("No internship updated. Possible unauthorized access or invalid ID.")

            conn.commit()
            return redirect(url_for('view_all_internships'))

        # GET request: Fetch current internship details
        cursor.execute("""
            SELECT *
            FROM internship
            WHERE internship_id = %s AND company_id = %s
        """, (internship_id, company_id))

        internship = cursor.fetchone()

        if not internship:
            return "Internship not found or unauthorized access.", 404

        return render_template('edit_internship.html', internship=internship)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('edit_internship.html', internship=request.form or internship, error=f"Database error: {err}"), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


@app.route('/company/internship/delete/<int:internship_id>', methods=['GET'])
def delete_internship(internship_id):
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM internship
        WHERE internship_id = %s AND company_id = %s
    """, (internship_id, company_id))

    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect(url_for('view_all_internships'))



@app.route('/company/feedback', methods=['GET', 'POST'])
def company_feedback():
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch interns who applied to the company's internships
        cursor.execute("""
            SELECT DISTINCT a.user_id, a.fname, a.lname
            FROM applicant a
            JOIN applications app ON a.user_id = app.user_id
            JOIN internship i ON app.internship_id = i.internship_id
            WHERE i.company_id = %s
        """, (company_id,))
        interns = cursor.fetchall()

        # Fetch feedback given by interns to the company
        cursor.execute("""
            SELECT f.feedback_id, f.feedback_text, f.rating, f.date_given, 
                   CONCAT(a.fname, ' ', a.lname) AS intern_name
            FROM feedback f
            JOIN applicant a ON f.user_id = a.user_id
            WHERE f.company_id = %s AND f.given_by = 'applicant'
            ORDER BY f.date_given DESC
        """, (company_id,))
        received_feedback = cursor.fetchall()

        # Get company email and name
        cursor.execute("SELECT email, company_name FROM company WHERE company_id = %s", (company_id,))
        company = cursor.fetchone()
        company_email = company['email']
        company_name = company['company_name']

        if request.method == 'POST':
            feedback_type = request.form.get('feedback_type')
            feedback_text = request.form.get('feedback_text')
            rating = request.form.get('rating')
            user_id = request.form.get('user_id') if feedback_type == 'intern' else None

            # Validate inputs
            if not feedback_text:
                return render_template('company_feedback.html', error="Feedback text is required.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400
            if not feedback_type or feedback_type not in ['xtern', 'intern']:
                return render_template('company_feedback.html', error="Invalid feedback type.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400
            if feedback_type == 'intern' and not user_id:
                return render_template('company_feedback.html', error="Please select an intern.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400

            try:
                rating_int = int(rating)
                if rating_int < 1 or rating_int > 5:
                    return render_template('company_feedback.html', error="Rating must be between 1 and 5.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400
            except (ValueError, TypeError):
                return render_template('company_feedback.html', error="Invalid rating format.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400

            if feedback_type == 'intern':
                cursor.execute("""
                    SELECT *
                    FROM applications app
                    JOIN internship i ON app.internship_id = i.internship_id
                    WHERE app.user_id = %s AND i.company_id = %s
                """, (user_id, company_id))
                if not cursor.fetchone():
                    return render_template('company_feedback.html', error="Selected intern is not associated with your internships.", interns=interns, received_feedback=received_feedback, company_name=company_name), 400

            # Insert feedback
            cursor.execute("""
                INSERT INTO feedback (user_id, company_id, given_by, feedback_text, rating, date_given)
                VALUES (%s, %s, 'company', %s, %s, NOW())
            """, (user_id, company_id, feedback_text, rating_int))
            conn.commit()

            # Email to Company
            subject_company = f"✅ Feedback Submitted: {feedback_type.capitalize()} Feedback"
            content_company = f"""
Hello {company_name},

Thank you for submitting your feedback on the {feedback_type}.

📌 **Feedback Details**:
- Type: {feedback_type.capitalize()}
- Rating: {rating_int}/5
- Feedback Text: {feedback_text}
- Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}

This confirmation ensures your feedback has been securely recorded.

Warm regards,  
Xtern Internship Portal
"""
            send_email(to=company_email, subject=subject_company, content=content_company, is_html=False)

            # Email to Intern (if applicable)
            if feedback_type == 'intern':
                cursor.execute("SELECT fname, lname, email FROM applicant WHERE user_id = %s", (user_id,))
                intern = cursor.fetchone()
                if intern:
                    intern_email = intern['email']
                    intern_name = f"{intern['fname']} {intern['lname']}"

                    subject_intern = "📢 Feedback Received from Company"
                    content_intern = f"""
Hello {intern_name},

You have received new feedback from **{company_name}** regarding your internship application.

📌 **Feedback Details**:
- Rating: {rating_int}/5
- Feedback Text: {feedback_text}
- Date: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}

This feedback is part of our continued effort to help you grow professionally.

All the best,  
Xtern Internship Portal
"""
                    send_email(to=intern_email, subject=subject_intern, content=content_intern, is_html=False)

            return redirect(url_for('company_dashboard'))

        return render_template('company_feedback.html', interns=interns, received_feedback=received_feedback, error=None, company_name=company_name)

    except mysql.connector.Error as err:
        return render_template('company_feedback.html', error=f"Database error: {err}", interns=[], received_feedback=[], company_name=company_name), 500
    except Exception as e:
        return render_template('company_feedback.html', error=f"An unexpected error occurred: {e}", interns=[], received_feedback=[], company_name=company_name), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            
                        

@app.route('/company/profile', methods=['GET', 'POST'])
def company_profile():
    if 'company_id' not in session:
        return redirect(url_for('login'))  # Adjust if you have a separate route

    company_id = session['company_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        industry = request.form['industry']
        website = request.form['website']
        contact_person = request.form['contact_person']
        contact_no = request.form['contact_no']

        cursor.execute("""
            UPDATE company
            SET company_name = %s, industry = %s, website_url = %s,
                contact_person = %s, contact_no = %s
            WHERE company_id = %s
        """, (name, industry, website, contact_person, contact_no, company_id))
        conn.commit()
        
        return redirect(url_for("company_dashboard"))

    cursor.execute("SELECT * FROM company WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('company_profile.html', company=company)



@app.route('/company/post_internship', methods=['GET', 'POST'])
def post_internship():
    if 'company_id' not in session:
        return redirect(url_for('login'))

    company_id = session['company_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch company email and name for the confirmation email
    cursor.execute("SELECT company_name, email FROM company WHERE company_id = %s", (company_id,))
    company_info = cursor.fetchone()

    if request.method == 'POST':
        title = request.form['title']
        post = request.form['post']
        description = request.form['description']
        duration = request.form['duration']
        required_skills = request.form['required_skills']
        main_subjects = request.form['main_subjects']
        minor_subjects = request.form['minor_subjects']
        stipend = request.form['stipend']
        location = request.form['location']
        remarks = request.form['remarks']
        open_date = request.form['open_date']
        close_date = request.form['close_date']
        job_offer = request.form['job_offer']

        # Set default status values
        internship_status = 'open'
        status = 'open'

        # Insert internship
        cursor.execute("""
            INSERT INTO internship (
                company_id, title, post, description, duration,
                required_skills, main_subjects, minor_subjects, stipend,
                location, remarks, internship_status, open_date, close_date,
                status, job_offer
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            company_id, title, post, description, duration,
            required_skills, main_subjects, minor_subjects, stipend,
            location, remarks, internship_status, open_date, close_date,
            status, job_offer
        ))

        conn.commit()

        # ✅ Send email to the company about the posting
        subject = f"Internship '{title}' Posted Successfully"
        content = f"""
Dear {company_info['company_name']},

Your internship post titled <b>{title}</b> has been successfully submitted on the Xtern platform.

Applicants will be able to view and apply once the internship opens on <b>{open_date}</b>.

Thank you for contributing to future careers!

Best regards,<br>
Xtern Team
"""
        send_email(
            to=company_info['email'],
            subject=subject,
            content=content,
            is_html=True
        )

        cursor.close()
        conn.close()
        return redirect(url_for('company_dashboard'))

    cursor.close()
    conn.close()
    return render_template('post_internship.html')



def fetch_and_combine_applicant_qualifications(user_id, cursor):
    """
    Fetch and combine qualifications (skills, main subjects, sub subjects) for an applicant.
    Args:
        user_id (int): ID of the applicant.
        cursor: Database cursor for executing queries.
    Returns:
        tuple: (combined_skills, combined_main_subjects, combined_sub_subjects) as strings.
    """
    # Fetch all qualifications for the user
    query = """
    SELECT skills, main_subjects, sub_subjects
    FROM user_qualification
    WHERE user_id = %s
    """
    cursor.execute(query, (user_id,))
    qualifications = cursor.fetchall()

    # Initialize lists to collect all skills and subjects
    all_skills = []
    all_main_subjects = []
    all_sub_subjects = []

    # Process each qualification record
    for qual in qualifications:
        # Split and clean skills
        if qual['skills']:
            skills = [skill.strip().lower() for skill in qual['skills'].split(',') if skill.strip()]
            all_skills.extend(skills)
        # Split and clean main subjects
        if qual['main_subjects']:
            main_subjects = [subject.strip().lower() for subject in qual['main_subjects'].split(',') if subject.strip()]
            all_main_subjects.extend(main_subjects)
        # Split and clean sub subjects
        if qual['sub_subjects']:
            sub_subjects = [subject.strip().lower() for subject in qual['sub_subjects'].split(',') if subject.strip()]
            all_sub_subjects.extend(sub_subjects)

    # Remove duplicates while preserving order
    all_skills = list(dict.fromkeys(all_skills))
    all_main_subjects = list(dict.fromkeys(all_main_subjects))
    all_sub_subjects = list(dict.fromkeys(all_sub_subjects))

    # Join back into comma-separated strings
    combined_skills = ', '.join(all_skills) if all_skills else ''
    combined_main_subjects = ', '.join(all_main_subjects) if all_main_subjects else ''
    combined_sub_subjects = ', '.join(all_sub_subjects) if all_sub_subjects else ''

    return combined_skills, combined_main_subjects, combined_sub_subjects


def calculate_skill_match_percentage(required_skills, main_subjects, minor_subjects, applicant_skills, applicant_main_subjects, applicant_sub_subjects):
    """
    Calculate the skill match percentage between internship requirements and applicant qualifications.
    Args:
        required_skills (str): Comma-separated string of required skills from internship.
        main_subjects (str): Comma-separated string of main subjects from internship.
        minor_subjects (str): Comma-separated string of minor subjects from internship.
        applicant_skills (str): Comma-separated string of applicant's skills.
        applicant_main_subjects (str): Comma-separated string of applicant's main subjects.
        applicant_sub_subjects (str): Comma-separated string of applicant's sub subjects.
    Returns:
        float: Percentage of matched skills and subjects (0.0 to 100.0).
    """
    # Normalize and split inputs into lists
    def normalize_list(text):
        if not text:
            return []
        return [item.strip().lower() for item in text.split(',') if item.strip()]

    # Normalize all required and applicant data
    required_skills_list = normalize_list(required_skills)
    main_subjects_list = normalize_list(main_subjects)
    minor_subjects_list = normalize_list(minor_subjects)
    applicant_skills_list = normalize_list(applicant_skills)
    applicant_main_subjects_list = normalize_list(applicant_main_subjects)
    applicant_sub_subjects_list = normalize_list(applicant_sub_subjects)

    # Combine all required items (skills + main subjects + minor subjects)
    all_required = required_skills_list + main_subjects_list + minor_subjects_list
    # Combine all applicant items (skills + main subjects + sub subjects)
    all_applicant = applicant_skills_list + applicant_main_subjects_list + applicant_sub_subjects_list

    # Remove duplicates while preserving order
    all_required = list(dict.fromkeys(all_required))
    all_applicant = list(dict.fromkeys(all_applicant))

    # If no required items, return 0 to avoid division by zero
    if not all_required:
        return 0.0

    # Count matched items
    matched_count = sum(1 for item in all_required if item in all_applicant)

    # Calculate percentage
    percentage = (matched_count / len(all_required)) * 100
    return round(percentage, 2)



@app.route('/admin/reports')
def admin_reports():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    


    conn = None
    cursor = None

    # Initialize template variables
    total_applications = 0
    total_internships = 0
    total_companies = 0
    total_applicants = 0
    total_approved = 0
    total_rejected = 0
    pending_apps = []
    report_data = []
    report_type = request.args.get('report', None)
    report_title = ''

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch summary counts (always needed)
        cursor.execute("SELECT COUNT(*) AS total_applications FROM applications")
        total_applications = cursor.fetchone()['total_applications']

        cursor.execute("SELECT COUNT(*) AS total_internships FROM internship")
        total_internships = cursor.fetchone()['total_internships']

        cursor.execute("SELECT COUNT(*) AS total_companies FROM company")
        total_companies = cursor.fetchone()['total_companies']

        cursor.execute("SELECT COUNT(*) AS total_applicants FROM applicant")
        total_applicants = cursor.fetchone()['total_applicants']

        cursor.execute("SELECT COUNT(*) AS total_approved FROM applications WHERE status = 'Approved'")
        total_approved = cursor.fetchone()['total_approved']

        cursor.execute("SELECT COUNT(*) AS total_rejected FROM applications WHERE status = 'Rejected'")
        total_rejected = cursor.fetchone()['total_rejected']

        # Fetch pending applications for summary view
        if not report_type:
            cursor.execute("""
                SELECT a.application_id, CONCAT(ap.fname, ' ', ap.lname) AS applicant_name, 
                       i.title AS internship_title, a.applied_on, a.status
                FROM applications a
                JOIN applicant ap ON a.user_id = ap.user_id
                JOIN internship i ON a.internship_id = i.internship_id
                WHERE a.status = 'Pending'
                ORDER BY a.applied_on DESC
                LIMIT 100
            """)
            pending_apps = cursor.fetchall()

        # Fetch detailed report data if a report type is specified
        if report_type:
            if report_type == 'applications':
                report_title = 'All Applications'
                cursor.execute("""
                    SELECT a.application_id, CONCAT(ap.fname, ' ', ap.lname) AS applicant_name, 
                           i.title AS internship_title, c.company_name AS company_name, 
                           a.applied_on, a.status
                    FROM applications a
                    JOIN applicant ap ON a.user_id = ap.user_id
                    JOIN internship i ON a.internship_id = i.internship_id
                    JOIN company c ON i.company_id = c.company_id
                    ORDER BY a.applied_on DESC
                """)
                report_data = cursor.fetchall()

            elif report_type == 'internships':
                report_title = 'All Internships Posted'
                cursor.execute("""
                    SELECT i.internship_id, i.title, c.company_name AS company_name, 
                           i.description, i.stipend, i.open_date, i.close_date
                    FROM internship i
                    JOIN company c ON i.company_id = c.company_id
                    ORDER BY i.open_date DESC
                """)
                report_data = cursor.fetchall()

            elif report_type == 'companies':
                report_title = 'All Companies'
                cursor.execute("""
                    SELECT c.company_id, c.company_name, c.email, c.contact_no, c.status,
                           CONCAT(ca.address_line, ', ', ca.area, ', ', ca.city, ', ', ca.state, ' ', ca.pincode) AS address
                    FROM company c
                    LEFT JOIN company_address ca ON c.company_id = ca.company_id
                    ORDER BY c.company_name ASC
                """)
                report_data = cursor.fetchall()

            elif report_type == 'applicants':
                report_title = 'All Applicants'
                cursor.execute("""
                    SELECT a.user_id, CONCAT(a.fname, ' ', a.lname) AS name, a.email, 
                        a.contact_no, d.degree_name, q.institute
                    FROM applicant a
                    LEFT JOIN (
                        SELECT q1.*
                        FROM user_qualification q1
                        JOIN (
                            SELECT user_id, MAX(qualification_id) AS max_qid
                            FROM user_qualification
                            GROUP BY user_id
                        ) q2 ON q1.user_id = q2.user_id AND q1.qualification_id = q2.max_qid
                    ) q ON a.user_id = q.user_id
                    LEFT JOIN degree d ON q.degree_id = d.degree_id
                    ORDER BY a.user_id ASC


                """)
                report_data = cursor.fetchall()

            elif report_type == 'approved':
                report_title = 'Approved Applications'
                cursor.execute("""
                    SELECT a.application_id, CONCAT(ap.fname, ' ', ap.lname) AS applicant_name, 
                           i.title AS internship_title, c.company_name AS company_name, 
                           a.applied_on, a.status
                    FROM applications a
                    JOIN applicant ap ON a.user_id = ap.user_id
                    JOIN internship i ON a.internship_id = i.internship_id
                    JOIN company c ON i.company_id = c.company_id
                    WHERE a.status = 'Approved'
                    ORDER BY a.applied_on DESC
                """)
                report_data = cursor.fetchall()

            elif report_type == 'rejected':
                report_title = 'Rejected Applications'
                cursor.execute("""
                    SELECT a.application_id, CONCAT(ap.fname, ' ', ap.lname) AS applicant_name, 
                           i.title AS internship_title, c.company_name AS company_name, 
                           a.applied_on, a.status
                    FROM applications a
                    JOIN applicant ap ON a.user_id = ap.user_id
                    JOIN internship i ON a.internship_id = i.internship_id
                    JOIN company c ON i.company_id = c.company_id
                    WHERE a.status = 'Rejected'
                    ORDER BY a.applied_on DESC
                """)
                report_data = cursor.fetchall()

        return render_template('admin_reports.html',
                               total_applications=total_applications,
                               total_internships=total_internships,
                               total_companies=total_companies,
                               total_applicants=total_applicants,
                               total_approved=total_approved,
                               total_rejected=total_rejected,
                               pending_apps=pending_apps,
                               report_type=report_type,
                               report_title=report_title,
                               report_data=report_data,
                               error=None)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('admin_reports.html',
                               total_applications=0,
                               total_internships=0,
                               total_companies=0,
                               total_applicants=0,
                               total_approved=0,
                               total_rejected=0,
                               pending_apps=[],
                               report_type=None,
                               report_title='',
                               report_data=[],
                               error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('admin_reports.html',
                               total_applications=0,
                               total_internships=0,
                               total_companies=0,
                               total_applicants=0,
                               total_approved=0,
                               total_rejected=0,
                               pending_apps=[],
                               report_type=None,
                               report_title='',
                               report_data=[],
                               error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conn and conn.is_connected():
            try:
                conn.close()
            except:
                pass
                
    

@app.route('/admin/feedback', methods=['GET'])
def admin_feedback():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
 

    conn = None
    cursor = None
    analytics = {
        'total_count': 0,
        'avg_rating': 0.0,
        'xtern_count': 0,
        'xtern_avg': 0.0,
        'company_to_intern_count': 0,
        'company_to_intern_avg': 0.0,
        'intern_to_company_count': 0,
        'intern_to_company_avg': 0.0,
        'rating_distribution': {
            'labels': ['1', '2', '3', '4', '5'],
            'datasets': {
                'xtern': [0] * 5,
                'company_to_intern': [0] * 5,
                'intern_to_company': [0] * 5
            }
        },
        'type_proportion': {
            'labels': ['Xtern', 'Company-to-Intern', 'Intern-to-Company'],
            'datasets': [0, 0, 0]
        }
    }

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True, buffered=True)

        # Fetch Xtern Platform Feedback (user_id IS NULL OR company_id IS NULL)
        cursor.execute("""
            SELECT f.given_by, f.feedback_text, f.rating, f.date_given
            FROM feedback f
            WHERE (f.user_id IS NULL OR f.company_id IS NULL) AND f.rating BETWEEN 1 AND 5
            ORDER BY f.date_given DESC
        """)
        xtern_feedback = cursor.fetchall()

        # Fetch Company-to-Intern Feedback
        cursor.execute("""
            SELECT c.company_name, CONCAT(a.fname, ' ', a.lname) AS intern_name,
                   f.feedback_text, f.rating, f.date_given
            FROM feedback f
            LEFT JOIN company c ON f.company_id = c.company_id
            LEFT JOIN applicant a ON f.user_id = a.user_id
            WHERE f.given_by = 'company' AND f.user_id IS NOT NULL AND f.rating BETWEEN 1 AND 5
            ORDER BY f.date_given DESC
        """)
        company_to_intern_feedback = cursor.fetchall()

        # Fetch Intern-to-Company Feedback
        cursor.execute("""
            SELECT CONCAT(a.fname, ' ', a.lname) AS intern_name, c.company_name,
                   f.feedback_text, f.rating, f.date_given
            FROM feedback f
            LEFT JOIN applicant a ON f.user_id = a.user_id
            LEFT JOIN company c ON f.company_id = c.company_id
            WHERE f.given_by = 'applicant' AND f.company_id IS NOT NULL AND f.rating BETWEEN 1 AND 5
            ORDER BY f.date_given DESC
        """)
        intern_to_company_feedback = cursor.fetchall()

        # Compute Analytics
        # Total Count and Overall Average Rating
        cursor.execute("""
            SELECT COUNT(*) AS count, ROUND(AVG(rating), 2) AS avg 
            FROM feedback 
            WHERE rating BETWEEN 1 AND 5
        """)
        total_data = cursor.fetchone()
        analytics['total_count'] = total_data['count']
        analytics['avg_rating'] = float(total_data['avg']) if total_data['avg'] is not None else 0.0


        # Xtern Feedback Stats
        cursor.execute("""
            SELECT COUNT(*) AS count, ROUND(AVG(rating), 2) AS avg 
            FROM feedback 
            WHERE (user_id IS NULL OR company_id IS NULL) AND rating BETWEEN 1 AND 5
        """)
        xtern_stats = cursor.fetchone()
        analytics['xtern_count'] = xtern_stats['count']
        analytics['xtern_avg'] = float(xtern_stats['avg']) if xtern_stats['avg'] is not None else 0.0


        # Company-to-Intern Feedback Stats
        cursor.execute("""
            SELECT COUNT(*) AS count, ROUND(AVG(rating), 2) AS avg 
            FROM feedback 
            WHERE given_by = 'company' AND user_id IS NOT NULL AND rating BETWEEN 1 AND 5
        """)
        company_to_intern_stats = cursor.fetchone()
        analytics['company_to_intern_count'] = company_to_intern_stats['count']
        analytics['company_to_intern_avg'] = float(company_to_intern_stats['avg']) if company_to_intern_stats['avg'] is not None else 0.0


        # Intern-to-Company Feedback Stats
        cursor.execute("""
            SELECT COUNT(*) AS count, COALESCE(AVG(rating), 0) AS avg 
            FROM feedback 
            WHERE given_by = 'applicant' AND company_id IS NOT NULL AND rating BETWEEN 1 AND 5
        """)
        intern_to_company_stats = cursor.fetchone()
        analytics['intern_to_company_count'] = intern_to_company_stats['count']
        analytics['intern_to_company_avg'] = float(intern_to_company_stats['avg'])

        # Rating Distribution
        # Xtern Rating Distribution
        cursor.execute("""
            SELECT rating, COUNT(*) AS count
            FROM feedback
            WHERE (user_id IS NULL OR company_id IS NULL) AND rating BETWEEN 1 AND 5
            GROUP BY rating
            ORDER BY rating
        """)
        xtern_data = {str(row['rating']): row['count'] for row in cursor.fetchall()}
        analytics['rating_distribution']['datasets']['xtern'] = [xtern_data.get(str(i), 0) for i in range(1, 6)]

        # Company-to-Intern Rating Distribution
        cursor.execute("""
            SELECT rating, COUNT(*) AS count
            FROM feedback
            WHERE given_by = 'company' AND user_id IS NOT NULL AND rating BETWEEN 1 AND 5
            GROUP BY rating
            ORDER BY rating
        """)
        company_to_intern_data = {str(row['rating']): row['count'] for row in cursor.fetchall()}
        analytics['rating_distribution']['datasets']['company_to_intern'] = [company_to_intern_data.get(str(i), 0) for i in range(1, 6)]

        # Intern-to-Company Rating Distribution
        cursor.execute("""
            SELECT rating, COUNT(*) AS count
            FROM feedback
            WHERE given_by = 'applicant' AND company_id IS NOT NULL AND rating BETWEEN 1 AND 5
            GROUP BY rating
            ORDER BY rating
        """)
        intern_to_company_data = {str(row['rating']): row['count'] for row in cursor.fetchall()}
        analytics['rating_distribution']['datasets']['intern_to_company'] = [intern_to_company_data.get(str(i), 0) for i in range(1, 6)]

        # Type Proportion
        analytics['type_proportion']['datasets'] = [
            analytics['xtern_count'],
            analytics['company_to_intern_count'],
            analytics['intern_to_company_count']
        ]

        return render_template('admin_feedback.html',
                             xtern_feedback=xtern_feedback,
                             company_to_intern_feedback=company_to_intern_feedback,
                             intern_to_company_feedback=intern_to_company_feedback,
                             analytics=analytics,
                             error=None)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return render_template('admin_feedback.html',
                             xtern_feedback=[],
                             company_to_intern_feedback=[],
                             intern_to_company_feedback=[],
                             analytics=analytics,
                             error=f"Database error: {err}"), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return render_template('admin_feedback.html',
                             xtern_feedback=[],
                             company_to_intern_feedback=[],
                             intern_to_company_feedback=[],
                             analytics=analytics,
                             error=f"An unexpected error occurred: {e}"), 500
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()            
            

# Route to render the analytics dashboard page
@app.route('/admin/analytics')
def admin_analytics():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    return render_template('admin_analytics.html')

# API route to return Applications Per Internship data
@app.route('/admin/report/applications_per_internship')
def applications_per_internship():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT i.title AS label, COUNT(a.application_id) AS count
        FROM internship i
        LEFT JOIN applications a ON i.internship_id = a.internship_id
        GROUP BY i.internship_id
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(data)




@app.route('/admin/report/internships_per_company')
def internships_per_company():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT c.company_name AS label, COUNT(i.internship_id) AS count
        FROM company c
        LEFT JOIN internship i ON c.company_id = i.company_id
        GROUP BY c.company_id
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)



@app.route('/admin/report/application_status_distribution')
def application_status_distribution():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT status AS label, COUNT(*) AS count
        FROM applications
        GROUP BY status
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)


@app.route('/admin/report/applications_by_degree')
def applications_by_degree():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT d.degree_name AS label, COUNT(a.application_id) AS count
        FROM applications a
        JOIN applicant ap ON a.user_id = ap.user_id
        JOIN user_qualification eq ON ap.user_id = eq.user_id
        JOIN degree d ON eq.degree_id = d.degree_id
        GROUP BY d.degree_name
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)


@app.route('/admin/report/monthly_application_trends')
def monthly_application_trends():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            DATE_FORMAT(applied_on, '%Y-%m') AS label, 
            COUNT(*) AS count
        FROM applications
        GROUP BY label
        ORDER BY label
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)



@app.route('/admin/report/top_5_companies_by_applications')
def top_5_companies_by_applications():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT c.company_name AS label, COUNT(a.application_id) AS count
        FROM applications a
        JOIN internship i ON a.internship_id = i.internship_id
        JOIN company c ON i.company_id = c.company_id
        GROUP BY c.company_id
        ORDER BY count DESC
        LIMIT 5
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)


@app.route('/admin/report/internships_posted_per_month')
def internships_posted_per_month():
    if 'admin_id' not in session:  # Uncomment for session-based authentication
        return redirect(url_for('admin_login'))
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            DATE_FORMAT(open_date, '%Y-%m') AS label,
            COUNT(internship_id) AS count
        FROM internship
        GROUP BY label
        ORDER BY label
    """
    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True)