import re

def validate_company_registration(form_data):
    errors = {}  # Dictionary to store field-specific errors

    # Validate Company Name (Only letters and spaces, required)
    if not form_data['company_name'].strip():
        errors['company_name'] = "Company name is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['company_name']):
        errors['company_name'] = "Company name should only contain letters and spaces."

    # Validate Industry Type (Only letters and spaces, required)
    if not form_data['industry'].strip():
        errors['industry'] = "Industry type is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['industry']):
        errors['industry'] = "Industry type should only contain letters and spaces."

    # Validate Contact Person (Only letters and spaces, required)
    if not form_data['contact_person'].strip():
        errors['contact_person'] = "Contact person's name is required."
    elif not re.fullmatch(r"^[A-Za-z\s]+$", form_data['contact_person']):
        errors['contact_person'] = "Contact person's name should only contain letters and spaces."

    # Validate Email (Required & Proper format)
    if not form_data['email'].strip():
        errors['email'] = "Email is required."
    elif not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", form_data['email']):
        errors['email'] = "Invalid email format."

    # Validate Contact Number (Exactly 10 digits, cannot start with 0)
    if not form_data['phone'].strip():
        errors['phone'] = "Contact number is required."
    elif not re.fullmatch(r"^[1-9][0-9]{9}$", form_data['phone']):
        errors['phone'] = "Contact number must be exactly 10 digits and cannot start with 0."

        
    if not form_data['website_url'].strip():
        errors['website_url'] = "Website URL is required."
    elif not re.fullmatch(r'^(https?:\/\/)([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$', form_data['website_url']):
        errors['website_url'] = "Invalid website URL format. It should start with http:// or https:// and be a valid domain."
        
    # Validate Pincode (Exactly 6 digits, required)
    if not form_data['pincode'].strip():
        errors['pincode'] = "Pincode is required."
    elif not re.fullmatch(r"^\d{6}$", form_data['pincode']):
        errors['pincode'] = "Pincode must be exactly 6 digits."

    # Validate Address Fields (Required)
    required_fields = ['address_line', 'city', 'state', 'area']
    for field in required_fields:
        if not form_data.get(field, "").strip():
            errors[field] = f"{field.replace('_', ' ').title()} is required."
            

    # Validate Password (At least 6 characters, must include letters and numbers)
    if not form_data['password'].strip():
        errors['password'] = "Password is required."
    elif not re.fullmatch(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$", form_data['password']):
        errors['password'] = "Password must be at least 6 characters long and contain both letters and numbers."

    # Validate Confirm Password (Must match Password)
    if form_data['password'] != form_data['confirm_password']:
        errors['confirm_password'] = "Passwords do not match."

    return errors  # Return dictionary with errors for each field




def validate_company_login(form_data):
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
