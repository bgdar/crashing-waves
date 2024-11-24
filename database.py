import sqlite3
from datetime import datetime

conn = sqlite3.connect("databases.db")
cursor = conn.cursor()
cursor.execute("""create table if not exists users(
                name text not null,
                password text not null)""")
 
# cursor.execute("insert into users (name, password) values ('dar','daraja')")
# cursor.execute("insert into users (name, password) values ('nadar','nadharaja')")


#================================================================
# table contact untuk pengelolaan contact
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contact(
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        name TEXT NOT NULL,
        email text NOT NULL,
        phone integer NOT NULL,
        age INTEGER
    )
''')

#cursor.execute("insert into contact ( name, email, phone ,age) values ('dar','dar@gmail.com',089523135244,19)")
#cursor.execute("insert into contact ( name, email, phone ,age) values ('jamal','jamal@gmail.com',085259156280,19)")

#cursor.execute("INSERT INTO contact (name,email,phone,age) SELECT name,email,phone,age FROM contact") buta tabel baru dan pindahkan  data

#cursor.execute("DELETE FROM contact WHERE id = ?", (1,)) dlete berdasar ID 
#cursor.execute("DELETE FROM contact where name='nadar'") #hapus semua baris
#cursor.execute("select * from sqlite_sequence")
#================================================================


cursor.execute('''
    CREATE TABLE IF NOT EXISTS todoContainer(
        text TEXT NOT NULL,
        user TEXT NOT NULL,
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
''') 
# cursor.execute("insert into todoContainer ( text, user) values ('catatan pertama','dar1')")

# comentar = 'Komentar pertama by dar'
# date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

#  Menjalankan query dengan placeholder ?
# cursor.execute("INSERT INTO todo (comentar, date) VALUES (?, ?)", (comentar, date))
#------------------------------------------

cursor.execute('DROP TABLE IF EXISTS todo') #perintah untuk menghpus table 
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")# lihat table apa aja
# cursor.execute("select * from users")
# cursor.execute("delete from todoContainer where id ='9'")
cursor.execute("select * from todoContainer")

data_table = cursor.fetchall()
for data in data_table:
    print(data)

conn.commit()
conn.close()
