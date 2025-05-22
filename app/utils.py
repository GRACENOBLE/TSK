from datetime import datetime, timedelta
from dateutil.parser import parse # You'll need to install python-dateutil
from dateutil.relativedelta import relativedelta # Also from python-dateutil
from typing import Optional

def parse_due_date(date_string: str) -> Optional[str]:
    """
    Parses a flexible date string (e.g., 'today', 'tomorrow', 'next week', '2025-12-31')
    into a 'YYYY-MM-DD' string. Returns None if parsing fails.
    """
    if not date_string:
        return None

    date_string_lower = date_string.lower().strip()
    today = datetime.now()

    try:
        if date_string_lower == "today":
            return today.strftime("%Y-%m-%d")
        elif date_string_lower == "tomorrow":
            return (today + timedelta(days=1)).strftime("%Y-%m-%d")
        elif date_string_lower == "next week":
            return (today + relativedelta(weeks=+1)).strftime("%Y-%m-%d")
        elif date_string_lower == "next month":
            return (today + relativedelta(months=+1)).strftime("%Y-%m-%d")
        elif date_string_lower == "next year":
            return (today + relativedelta(years=+1)).strftime("%Y-%m-%d")
        # Add more common phrases as needed

        # Attempt to parse general dates
        # fuzzy=True allows some flexibility (e.g., "May 22" will parse)
        parsed_date = parse(date_string, fuzzy=True)
        return parsed_date.strftime("%Y-%m-%d")

    except ValueError:
        # dateutil.parser.parse can raise ValueError if it can't parse the string
        return None # Indicate parsing failure

def get_today_str() -> str:
    """Returns today's date as a 'YYYY-MM-DD' string."""
    return datetime.now().strftime("%Y-%m-%d")