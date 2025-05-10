from langchain.agents import tool

@tool
def book_appointment(name: str, email: str, phone: str, date: str):
    """Books an appointment for a user. All fields must be validated."""
    # Simulate action (can be replaced with DB/API)
    return f"Appointment booked for {name} on {date}. Confirmation sent to {email}."
