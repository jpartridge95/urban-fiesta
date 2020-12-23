import sqlite3

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



