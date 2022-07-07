import bcrypt
pwd = "123456"
pwd = pwd.encode('utf-8')
hashed = bcrypt.hashpw(pwd, bcrypt.gensalt(10))
check = "123486"
check = check.encode('utf-8')
if bcrypt.checkpw(check,hashed):
    print("Yes")
else:
    print("No")