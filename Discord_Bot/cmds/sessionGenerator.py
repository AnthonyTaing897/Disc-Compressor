import random
import string
import gspread
from datetime import datetime, timedelta

characters = string.ascii_letters + string.digits

def gen_code(length):
    return ''.join(random.choice(characters) for _ in range(length))

def gen_sessCode(length=6, database=None):       
    code = gen_code(length)

    if(database):
        database.get_all_records()
        for record in database.get_all_records():
            if record['Given Code'] == code:
                return gen_sessCode(length,database)
        
    return code
    
def gen_sessID(length=10, database=None):        
    code = gen_code(length)

    if(database):
        database.get_all_records()
        for record in database.get_all_records():
            if record['Session ID'] == code:
                return gen_sessID(length,database)
        
    return code

def create_session(userID:str, database:gspread.Worksheet) -> str:
            session_ID = gen_sessID(database=database)
            session_code = gen_sessCode(database=database)

            utc_1h_time = datetime.utcnow() + timedelta(hours=1)

            if database is None:
                raise ValueError("Database worksheet is not provided.")
            
            # Store session in the database sets date and time automatically separately
            database.append_row([session_ID, session_code, str(userID), str(utc_1h_time.date().strftime("%Y-%m-%d")), str(utc_1h_time.time().strftime("%H:%M:%S")),0])

            return session_code

def user_exists(userID:str, database:gspread.Worksheet) -> bool:
        records = database.get_all_records()
        for record in records:
            if str(record['User ID']) == str(userID):
                return True
        return False
    
def user_exists_but_inactive(userID:str, database:gspread.Worksheet) -> bool:
    records = database.get_all_records()
    for record in records:
        if str(record['User ID']) == str(userID):
            # Check if the session is still active (within 1 hour)
            session_time_str = f"{record['Date (UTC)']} {record['Time (UTC)']}"
            session_time = datetime.strptime(session_time_str, "%Y-%m-%d %H:%M:%S")
            if datetime.utcnow() > session_time:
                return True
    return False