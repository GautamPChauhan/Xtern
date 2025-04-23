import re

def validate_applicant_registration(form_data):
    errors = {}

    # First Name
    if not form_data['fname'].strip():
        errors['fname'] = "First name is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['fname']):
        errors['fname'] = "First name should contain only letters and spaces."

    # Last Name
    if not form_data['lname'].strip():
        errors['lname'] = "Last name is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['lname']):
        errors['lname'] = "Last name should contain only letters and spaces."

    # Date of Birth
    if not form_data['dob'].strip():
        errors['dob'] = "Date of birth is required."
    elif not re.fullmatch(r"^\d{4}-\d{2}-\d{2}$", form_data['dob']):
        errors['dob'] = "Date of birth must be in YYYY-MM-DD format."

    # Contact Number
    if not form_data['contact_no'].strip():
        errors['contact_no'] = "Contact number is required."
    elif not re.fullmatch(r"^[6-9]\d{9}$", form_data['contact_no']):
        errors['contact_no'] = "Enter a valid 10-digit phone number starting with 6-9."

    # Email
    if not form_data['email'].strip():
        errors['email'] = "Email is required."
    elif not re.fullmatch(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", form_data['email']):
        errors['email'] = "Invalid email format."

    # City
    if not form_data['city'].strip():
        errors['city'] = "City is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['city']):
        errors['city'] = "City should only contain letters and spaces."

    # State
    if not form_data['state'].strip():
        errors['state'] = "State is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['state']):
        errors['state'] = "State should only contain letters and spaces."

    # Password
    if not form_data['password'].strip():
        errors['password'] = "Password is required."
    elif not re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", form_data['password']):
        errors['password'] = "Password must be at least 6 characters long and contain both letters and numbers."


    # Confirm Password
    if not form_data['confirm_password'].strip():
        errors['confirm_password'] = "Confirm password is required."
    elif form_data['password'] != form_data['confirm_password']:
        errors['confirm_password'] = "Passwords do not match."

    # # Resume URL / File
    # if not form_data['resume_url'].strip():
    #     errors['resume_url'] = "Resume is required."
    # elif not re.fullmatch(r".+\.(pdf|doc|docx)$", form_data['resume_url']):
    #     errors['resume_url'] = "Resume must be a .pdf, .doc, or .docx file."

    return errors




def validate_applicant_login(form_data):
    errors = {}

    # Validate email
    email = form_data.get('email', '').strip()
    if not email:
        errors['email'] = "Email is required."
    elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        errors['email'] = "Invalid email format."

    # Validate password
    password = form_data.get('password', '').strip()
    if not password:
        errors['password'] = "Password is required."
    elif not re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", form_data['password']):
        errors['password'] = "Password must be at least 6 characters long and contain both letters and numbers."


    # Validate user type
    user_type = form_data.get('user_type', '')
    if not user_type:
        errors['user_type'] = "User type is required."

    return errors
