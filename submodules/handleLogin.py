import mysql.connector as db

conn = db.connect(
	host = "localhost",
    user = "root",
    password="",
    database = "recomovies"
)

def doLogin(username,password):
	cursor = conn.cursor()
	sql = f"SELECT * FROM user WHERE username = '{username.lower()}'"
	cursor.execute(sql)
	records = cursor.fetchall()
	if not records:
		return False,f"No registered username as {username}!"
	if not (password == records[0][6]):
		return False,f"Password doesn't seem to match. Please try again."
	return True,None




