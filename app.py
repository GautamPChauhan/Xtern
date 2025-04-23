
import mysql.connector
from flask import Flask, request, redirect, url_for, flash, render_template, session
from modules.company import validate_company_registration, validate_company_login
from werkzeug.security import generate_password_hash, check_password_hash
from modules.applicant import validate_applicant_registration, validate_applicant_login
import os
from werkzeug.utils import secure_filename
from datetime import date


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
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if the user has submitted qualifications
    cursor.execute("SELECT * FROM user_qualification WHERE user_id = %s", (user_id,))
    qualification = cursor.fetchone()
    has_qualification = qualification is not None

    internships = []
    if has_qualification:
        cursor.execute("""
            SELECT i.*, c.company_name, c.website_url
            FROM internship i
            JOIN company c ON i.company_id = c.company_id
            WHERE i.status = 'Open'
        """)
        internships = cursor.fetchall()

        # Check if the user has applied to each internship
        for internship in internships:
            cursor.execute("""
                SELECT status FROM applications
                WHERE user_id = %s AND internship_id = %s
                ORDER BY applied_on DESC LIMIT 1
            """, (user_id, internship['internship_id']))
            application = cursor.fetchone()

            if application:
                internship['applied'] = True
                internship['application_status'] = application['status']
            else:
                internship['applied'] = False
                internship['application_status'] = None

    cursor.close()
    conn.close()

    return render_template('applicant_dashboard.html', has_qualification=has_qualification, internships=internships)




@app.route('/apply/<int:internship_id>', methods=['POST'])
def apply_internship(internship_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch internship details
    cursor.execute("SELECT required_skills, main_subjects, minor_subjects, open_date FROM internship WHERE internship_id = %s", (internship_id,))
    internship = cursor.fetchone()

    if not internship:
        cursor.close()
        conn.close()
        return redirect(url_for('applicant_dashboard', msg='Internship not found.'))

    # Check if internship is open
    if internship['open_date'] >= date.today():
        msg = f"You can apply after the internship opens on {internship['open_date'].strftime('%Y-%m-%d')}"
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
    cursor.execute("SELECT status FROM applications WHERE user_id = %s AND internship_id = %s", (user_id, internship_id))
    existing_application = cursor.fetchone()

    if existing_application:
        # Allow re-application if the previous application is Withdrawn or Rejected
        if existing_application['status'] in ['Withdrawn', 'Rejected']:
            # Insert a new application
            cursor.execute("""
                INSERT INTO applications (user_id, internship_id, applied_on, status, skill_match_percentage)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, internship_id, date.today(), 'Pending', skill_match_percentage))
        else:
            # Existing application is active (e.g., Pending, Accepted)
            cursor.close()
            conn.close()
            return redirect(url_for('applicant_dashboard', msg='You have already applied for this internship.'))

    else:
        # No existing application, insert a new one
        cursor.execute("""
            INSERT INTO applications (user_id, internship_id, applied_on, status, skill_match_percentage)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, internship_id, date.today(), 'Pending', skill_match_percentage))

    conn.commit()
    cursor.close()
    conn.close()

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
    cursor.execute("SELECT * FROM applications WHERE application_id = %s AND user_id = %s", (application_id, user_id))
    application = cursor.fetchone()

    if application and application['status'] == 'Pending':
        # Update the application status to withdrawn
        cursor.execute("UPDATE applications SET status = 'Withdrawn' WHERE application_id = %s", (application_id,))
        conn.commit()
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



@app.route('/applicant/update_qualification', methods=['GET', 'POST'])
def update_qualification():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
            WHERE user_id=%s
        """, (degree_id, year, board, percentage, main_subjects, sub_subjects, skills, interest, institute, user_id))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('applicant_myqualifications'))

    # GET request: prefill form with existing data
    cursor.execute("""
        SELECT * FROM user_qualification WHERE user_id = %s
    """, (user_id,))
    qualification = cursor.fetchone()

    cursor.execute("SELECT * FROM degree")
    degrees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("update_qualification.html", qualification=qualification, degrees=degrees)

@app.route('/applicant/profile', methods=['GET', 'POST'])
def applicant_profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('applicant_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        # Get updated form data
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        phone = request.form.get('phone')
        city = request.form.get('city')
        state = request.form.get('state')

        # Update in database
        cursor.execute("""
            UPDATE applicant 
            SET fname = %s, lname = %s, contact_no = %s, city = %s, state = %s 
            WHERE user_id = %s
        """, (fname, lname, phone, city, state, user_id))
        conn.commit()
        
        return redirect(url_for("applicant_dashboard"))

    # Fetch latest profile info
    cursor.execute("SELECT * FROM applicant WHERE user_id = %s", (user_id,))
    applicant = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('applicant_profile.html', applicant=applicant)



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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT i.*, 
               (DATEDIFF(i.close_date, CURDATE())) AS days_left,
               (SELECT COUNT(*) FROM applications a WHERE a.internship_id = i.internship_id) AS applicant_count
        FROM internship i
        WHERE i.company_id = %s
        ORDER BY i.open_date DESC
    """, (company_id,))
    
    internships = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('company_dashboard.html', internships=internships)




@app.route('/company/applications')
def company_applications():
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all applications for internships posted by this company
    cursor.execute("""
            SELECT 
                a.application_id, a.status AS application_status, a.skill_match_percentage, a.remarks, a.applied_on,
                u.user_id, u.fname AS applicant_name, u.email, u.contact_no, u.city, u.state,
                i.internship_id, i.title AS internship_title, i.post, i.location, 
                i.description AS internship_description, i.stipend, i.duration,
                c.company_name, c.website_url
            FROM applications a
            JOIN applicant u ON a.user_id = u.user_id
            JOIN internship i ON a.internship_id = i.internship_id
            JOIN company c ON i.company_id = c.company_id
            WHERE i.company_id = %s
            ORDER BY a.application_id DESC
        """, (company_id,))
    
    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('company_applications.html', applications=applications)


@app.route('/company/approve_application/<int:application_id>', methods=['POST'])
def approve_application(application_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = 'Approved' WHERE application_id = %s", (application_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('company_applications'))

@app.route('/company/reject_application/<int:application_id>', methods=['POST'])
def reject_application(application_id):
    company_id = session.get('company_id')
    if not company_id:
        return redirect(url_for('company_login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = 'Rejected' WHERE application_id = %s", (application_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('company_applications'))




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

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_all_internships'))

    # GET request: Fetch current internship details
    cursor.execute("""
        SELECT *
        FROM internship
        WHERE internship_id = %s AND company_id = %s
    """, (internship_id, company_id))

    internship = cursor.fetchone()
    cursor.close()
    conn.close()

    if internship:
        return render_template('edit_internship.html', internship=internship)
    else:
        return "Internship not found or unauthorized access.", 404



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
    cursor = conn.cursor()

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
        internship_status = 'Open'
        status = 'Open'

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



if __name__ == '__main__':
    app.run(debug=True)
