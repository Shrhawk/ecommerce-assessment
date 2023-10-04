from datetime import datetime
from fastapi import HTTPException


def parse_date(date_str):
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use ISO date format (YYYY-MM-DD).")
