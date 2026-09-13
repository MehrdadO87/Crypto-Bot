def login():
	username_entry = input("enter the username: ")
	password_entry = input("enter the password: ")

	username = username_entry
	password = password_entry

	if username == "admin" and password == "password":
		print("login successfully")
	else:
		print("invalid username or password")



login()
