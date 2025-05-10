from dateutil import parser
from datetime import datetime, timedelta
import dateutil.relativedelta as rd

def parse_date(text):
    try:
        dt = parser.parse(text, fuzzy=True)
        return dt.date().isoformat()
    except:
        return "Invalid date"
