import sqlite3, hashlib, binascii, os, pandas
from pathlib import Path

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
            auth text
        )""")
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

#def new_user():

#def login():

#def check_auth():

#def parent_check_record():

#def server_comm():

#def run():


# Auth types, admin, teacher, parent. Goal to use this as a shared teacher parent metrics system, 
# however at this stage, unlikely as should have used smaller functions and nested them.  