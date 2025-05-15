from datetime import datetime, timedelta
from dateparser import parse

def parse_date(date_str: str) -> str:
    """Convert natural language dates to YYYY-MM-DD format"""
    date_obj = parse(date_str)
    if not date_obj:
        raise ValueError("Could not parse date")
    return date_obj.strftime("%Y-%m-%d")

def is_future_date(date_str: str) -> bool:
    """Check if date is in the future"""
    return datetime.strptime(date_str, "%Y-%m-%d") > datetime.now()