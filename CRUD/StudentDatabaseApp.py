import sqlite3, hashlib, binascii, os, pandas
from pathlib import Path

current_auth = "unnassigned"
current_user = "unnassigned"

def add_student():
    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()
    
    inp_name = str(input("Enter Student Name: "))
    inp_year = int(input("What year is " + inp_name + " in: "))
    inp_gender = str(input("Enter Gender: "))
    inp_class = str(input("Enter the student's class: "))
    inp_pgrade = float(input("Enter student's predicted grade: "))
    inp_cgrade = float(input("Enter student's current grade: "))
    inp_homework = str("_/_/_/_/_/_/_")
    inp_sen = str(input("Does the student have special educational needs? if so describe them: "))
    inp_comment = str(input("Enter a comment here: "))
    
    student = [
        inp_name,
        inp_gender,
        inp_year,
        inp_class,
        inp_pgrade,
        inp_cgrade,
        inp_homework,
        inp_sen,
        inp_comment
    ]
    
    c.execute("INSERT INTO Students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", student)
    
    conn.commit()
    conn.close()
    

def search_student():
    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()
    
    response = input("[1] Search by name \n[2] Search by attribute \n[3] Return all\n...")
    if response == 1:
        search = input("Enter the student's name: ")
        for row in c.execute("SELECT * FROM Students WHERE name = ?", search):
            print (row)        
    elif response == 2:
        search_attribute = input("""Which attribute do you want to search by? \n
        name \ngender \nyeargroup \nclass \npredictedgrade \n
        workingatgrade \nhomeworkin \nSEN \nOtherComments \n...""")
        search_query = input("Enter search term: ")
        for row in c.execute("SELECT * FROM Students WHERE ? = ?", (search_attribute, search_query)):
            print (row)
    elif response == 3:
        for row in c.execute("SELECT * FROM Students"):
            print (row)
    else:
        print ("Please enter either 1, 2 or 3")
        repeat = input("Do you wish to try again? y/n: ")
        if repeat == "y" or repeat == "Y":
            search_student()
    
    conn.close()

def remove_student():
    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()
    #Student lookup
    search = input("Enter the student's name: ")
    for row in c.execute("SELECT rowid, * FROM Students WHERE name = ?", search):
        print (row)
    row_identifier = input("Enter the student's unique identification number: ")
    #Student Delete
    c.execute("DELETE FROM Students WHERE rowid = ?", row_identifier)
    
    conn.commit()
    conn.close()

def edit_student_file():
    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()
    search = input("Enter the name of the student who's file you wish to edit: ")
    for row in c.execute("SELECT rowid, * FROM Students WHERE name = ?", search):
        print (row)
    row_identifier = input("Enter the student's unique identification number: ")
    which = input("""Which field do you wish to edit?  \n
        name \ngender \nyeargroup \nclass \npredictedgrade \n
        workingatgrade \nhomeworkin \nSEN \nOtherComments \n...""")
    new_val = input("What should the new value be? ")
    c.execute("""UPDATE Students SET ? = ? WHERE rowid = ?""", (which, new_val, row_identifier))
    conn.commit()
    conn.close()
    
    

def import_db():
    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()
    safety = input("WARNING, before you do this ensure you have made a copy. Do you wish to proceed? y/n: ")
    if safety != "y" and safety != "Y":
        print ("Response recieved, aborting operation")
        return
    file_name = input("Please specify a file path with valid extension: ")
    db_vals_csv = pandas.readcsv(file_name)
    db_vals_csv.to_sql("Students", conn, if_exists="append", index = False)
    conn.commit()
    conn.close()
    

def initialise_files():
    if Path("studentdb.db").is_file():
        print ("studentdb.db already exists")
    else:
        print ("Initialising file studentdb.db")
        conn = sqlite3.connect("studentdb.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE Students(
            name text,
            gender text,
            yeargroup integer,
            class text,
            predictedgrade real,
            workingatgrade real,
            homeworkin text,
            SEN text,
            OtherComments text
        )""")
        conn.commit()
        conn.close()
    if Path("userinfo.db").is_file():
        print ("User database already exists")
    else:
        print ("Initialising file userinfo.db")
        conn = sqlite3.connect("userinfo.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE UserInfo(
            username text,
            email text,
            password text,
            auth text,
            UNIQUE(username)
        )""")
        conn.commit()
        conn.close()
    if Path("parentdb.db").is_file():
        print ("Parent database already exists")
    else:
        print ("Initialising file parentdb.db")
        conn = sqlite3.connect("parentdb.db")
        c = conn.cursor()
        c.execute("""CREATE TABLE Parents(
            name text,
            username text,
            child integer,
            email text,
            phone text
        """)
        conn.commit()
        conn.close()
    
    conn = sqlite3.connect("userinfo.db")
    c = conn.cursor()
    admin_pass = hash_password("admin")
    default_admin = ["admin", "none", admin_pass, "admin"]
    c.execute("""INSERT INTO UserInfo VALUES (?, ?, ?, ?)""", (default_admin))
    conn.commit()
    conn.close()

def hash_password(password):
# personal, creates 256 bit hash from random stream of bytes, returns hexidecimal form of those bytes converted to utf-8
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    # personal using hashlibrary to hash using sha256 using the generated salt 100000 times
    pass_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    # personal converting the hashed pw back to hexidecimal
    pass_hash = binascii.hexlify(pass_hash)
    # personal combining both salt and hashed pw and decoding from utf-8
    return (salt + pass_hash).decode("ascii")

def check_password(provided_pass, stored_pass):
    salt = stored_pass[:64]
    password = stored_pass[64:]
    pass_hash = hashlib.pbkdf2_hmac("sha256", provided_pass.encode("utf-8"), salt, 100000)
    pass_hash = binascii.hexlify(pass_hash).encode("ascii")
    return (pass_hash == password)

def new_user():
    conn = sqlite3.connect("userinfo.db")
    c = conn.cursor()

    inp_username = str(input("Enter a username: "))
    inp_email = str(input("Enter your email: "))
    inp_password = str(input("Choose a password: "))
    pass_check = str(input ("Re-enter your password: "))
    auth = "unnassigned"

    while inp_password != pass_check:
        print ("Passwords do not match, try retyping your passwords")
        inp_password = str(input("Re-type your password: "))
        pass_check = str(input("Confirm your password: "))

    hashed_pass = hash_password(inp_password)

    new_user = [
        inp_username,
        inp_email,
        hashed_pass,
        auth
    ]

    try:
        c.execute("""INSERT INTO UserInfo VALUES (?, ?, ?, ?)""", new_user)
    except:
        print ("""Error whilst adding information to database, its likely your username is taken.""")
        new_user[0] = input("Please enter a new username: ")
        c.execute("""INSERT INTO UserInfo VALUES (?, ?, ?, ?)""", new_user)
    conn.commit()
    conn.close()


def login():
    conn = sqlite3.connect("userinfo.db")
    c = conn.cursor()

    global current_user
    global current_auth

    inp_username = input("Enter your username: ")
    inp_password = input("Enter your password: ")
    stored_pass = c.execute("""SELECT password FROM UserInfo WHERE username = ?""", inp_username)

    if check_password(inp_password, stored_pass):
        current_user = c.execute("""SELECT username FROM UserInfo WHERE username = ?""", inp_username)
        current_auth = c.execute("""SELECT auth FROM UserInfo WHERE username = ?""", inp_username)
    else:
        print ("Login failed please try again.")
    
    conn.close()

def check_auth(level_string):
    return level_string == current_auth

def assign_auth():
    conn = sqlite3.connect("userinfo.db")
    c = conn.cursor()
    inp_username = input("Enter the username of the profile you wish to edit permissions of: ")
    inp_auth = int(input("""Which access level do you want to grant %s?\n
    [1] admin\n
    [2] teacher\n
    [3] parent\n
    ...""", inp_username))
    if inp_auth == 1:
        auth_val = "admin"
    elif inp_auth == 2:
        auth_val = "teacher"
    elif inp_auth == 3:
        auth_val = "parent"
    else:
        print("Please enter 1, 2 or 3 for the corresponding value")
    c.execute("""UPDATE UserInfo SET auth = ? WHERE username = ?""", (auth_val, inp_username))
    
    conn.commit()
    conn.close()

def add_parent():
    conn = sqlite3.connect("parentdb.db")
    c = conn.cursor()

    inp_name = str(input("Enter the parent's name: "))
    inp_username = str(input("Enter the parent's username: "))
    inp_child_rowid = int(input("What child rowid is this parent entry assigned to? "))
    inp_email = str(input("Enter the parent's email: "))
    inp_phone = str(input("Enter the parent's phone number: "))

    new_parent = [
        inp_name,
        inp_username,
        inp_child_rowid,
        inp_email,
        inp_phone
    ]

    c.execute("""INSERT into Parents VALUES (?, ?, ?, ?, ?)""", (new_parent))

    conn.commit()
    conn.close()

def parent_check_record():
    conn = sqlite3.connect("parentdb.db")
    c = conn.cursor()
    global current_user
    child_id = []

    if current_user == "unnassigned":
        print ("Log in to access child records")
        return
    c.executemany("""RETURN child FROM Parents WHERE username = ?""", current_user)
    for child in c.fetchall():
        child_id.append(child)
    conn.close()

    conn = sqlite3.connect("studentdb.db")
    c = conn.cursor()

    for i in child_id:
        c.execute("""RETURN name, class, predictedgrade, homeworkin, OtherComments FROM Students WHERE rowid = ?""", i)
        print (c.fetchone())
    
    conn.close()

def remove_user():
    conn = sqlite3.connect("userinfo.db")
    c = conn.cursor()
    user_input = str(input("Enter the username of the user you wish to delete: "))

    c.execute("""DELETE FROM UserInfo WHERE username = ?""", user_input)
    conn.commit()
    conn.close()


def run():
    user_input = 1
    while user_input != 0:
        user_input = int(input("""What do you wish to do:\n
        [1] Login\n
        [2] Go to menus\n
        [3] Do this if this is your first time running the program\n
        [0] Exit program\n
        ..."""))
        if user_input == 1:
            login()
        elif user_input == 2:
            user_input = int(input("""Are you:\n
            [1] Teacher\n
            [2] Parent\n
            [3] Administrator\n
            [0] Exit Program\n
            ..."""))
            if user_input == 1 and check_auth("teacher"):
                user_input = int(input("""What do you wish to do?\n
                [1] Search for a student's records\n
                [2] Edit a student's records\n
                [3] Add a new student to the database\n
                [0] Exit Program\n
                ..."""))
                if user_input == 1:
                    search_student()
                elif user_input == 2:
                    edit_student_file()
                elif user_input == 3:
                    add_student()
            elif user_input == 2 and check_auth("parent"):
                user_input = int(input("""What do you wish to do?\n
                [1] Retrieve your child's records\n
                [0] Exit Program\n
                ..."""))
                if user_input == 1:
                    parent_check_record()
            elif user_input == 3 and check_auth("admin"):
                user_input = int(input("""What do you wish to do?\n
                [1] Search for a student's records\n
                [2] Edit a student's records\n
                [3] Add a student to the database\n
                [4] Delete a student from the database\n
                [5] Retrieve records from a parent perspective\n
                [6] Add user to user database\n
                [7] Remove user from database\n
                [8] Add parent to parent database\n
                [9] Assign authorisation\n
                [10] Import a csv file to student database\n
                [0] Exit Program\n
                ..."""))
                if user_input == 1:
                    search_student()
                elif user_input == 2:
                    edit_student_file()
                elif user_input == 3:
                    add_student()
                elif user_input == 4:
                    remove_student()
                elif user_input == 5:
                    parent_check_record()
                elif user_input == 6:
                    new_user()
                elif user_input == 7:
                    remove_user()
                elif user_input == 8:
                    add_parent()
                elif user_input == 9:
                    assign_auth()
                elif user_input == 10:
                    import_db()
        elif user_input == 3:
            boot_auth = str(input("Enter the password to initialise files: "))
            if boot_auth == "StrawberryLaces":
                initialise_files()
                

# Perhaps a function to open and close connections would have saved time.
# Auth types, admin, teacher, parent, unnassigned. Goal to use this as a shared teacher parent metrics system, 
# however at this stage, unlikely as should have used smaller functions and nested them 