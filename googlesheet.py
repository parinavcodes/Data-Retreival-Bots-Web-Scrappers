import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope=['https://www.googleapis.com/auth/drive']
credentials=ServiceAccountCredentials.from_json_keyfile_name('sheetn.json',scope)
client=gspread.authorize(credentials)
sheet=client.open('sheet').sheet1
a=sheet.get_all_records()
row_val=sheet.cell(1,1).value
print(row_val)
sheet.update_cell(1,2,'update')