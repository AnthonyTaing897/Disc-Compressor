import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]

creds = ServiceAccountCredentials.from_json_keyfile_name("disc-compress-cred.json", scope)

client = gspread.authorize(creds)


def initDatabase():
    return client.open("Disc_Compress_Requests").sheet1


if __name__ == "__main__":
    sheet = initDatabase()
    sheet.insert_row(["Test1", "Test2", "Test3"], 2)