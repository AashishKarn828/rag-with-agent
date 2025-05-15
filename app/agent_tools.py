from langchain.agents import tool
from app.form_tools import validate_name, validate_email_input, validate_phone
from app.date_utils import parse_date, is_future_date

@tool
def book_appointment(name: str, email: str, phone: str, date: str):
    """Books an appointment for a user. Validates all fields before booking."""
    # Validate inputs
    if not validate_name(name):
        return "Please provide a valid name"
    if not validate_email_input(email):
        return "Please provide a valid email"
    if not validate_phone(phone):
        return "Please provide a valid phone number"
    
    try:
        formatted_date = parse_date(date)
        if not is_future_date(formatted_date):
            return "Please provide a future date"
    except ValueError as e:
        return str(e)
    
    # If all validations pass
    return f"Appointment booked for {name} on {formatted_date}. Confirmation sent to {email}."

# New tool for handling callback requests
@tool
def request_callback(user_info: dict):
    """Collects and validates user info for callback requests in a conversational way."""
    required = ['name', 'email', 'phone']
    missing = [field for field in required if field not in user_info or not user_info[field]]

    # Ask for any missing fields one at a time
    if missing:
        return f"To schedule a callback, I need your {', '.join(missing)}."

    # Validate
    if not validate_name(user_info['name']):
        return "Please provide a valid name"
    if not validate_email_input(user_info['email']):
        return "Please provide a valid email"
    if not validate_phone(user_info['phone']):
        return "Please provide a valid phone number"

    return f"Thanks {user_info['name']}! We’ll contact you soon at {user_info['phone']}."
