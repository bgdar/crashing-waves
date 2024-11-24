import sqlite3
import datetime as dt

class get_db():
    def connect(self):
        conn = sqlite3.connect('databases.db')
        return conn
    #table users
    def read_tb_users(self, name, password):
        conn = self.connect() #membuat dan mengembalikan sebuah objek koneksi dari SQLite, yang merupakan instance dari sqlite3.Connection.
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE name=? AND password=?", (name, password))
        data = cursor.fetchone() # baca 1 baris
        conn.close()  # Make sure to close the connection
        return data
    def write_tb_users(self, name, password):
        conn = self.connect() #membuat dan mengembalikan sebuah objek koneksi dari SQLite, yang merupakan instance dari sqlite3.Connection.
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name,password) values (?,?)", (name, password))
        conn.commit()  # Simpan perubahan yang dilakukan.  
        conn.close() # Make sure to close the connection

    #table contact
    def read_tb_contact(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM contact ")
        data_table = cursor.fetchall()
        conn.close()
        return data_table
    def read_tb_contact_id(self,id_contact):
    # cari dan baca data berdasarkan id data yg di kirim
        conn = self.connect()
        cursor= conn.cursor()
        cursor.execute("SELECT * FROM contact WHERE id=?", (id_contact,))
        data =cursor.fetchone()
        conn.close()
        return data
    def write_tb_contact(self, name, email, phone,age):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("insert into contact (name,email,phone,age) values (?,?,?,?)", (name, email, phone,age))
        conn.commit()
        conn.close()
    # hapus data berdasarkan ID 
    def update_tb_contact(self,id,name,email,phone,age):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE contact SET name=?, email=?, phone=?, age=? WHERE id=?", (name, email, phone,age,id))
        conn.commit()
        conn.close()
    def delete_tb_contact_id(self,id_contact):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contact WHERE id=?", (id_contact,))
        conn.commit()
        conn.close()

    #table Container untuk todo
    def read_tb_todoContainer(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todoContainer ")
        data_table = cursor.fetchall()
        conn.close()
        return data_table
    def read_tb_todoContainer_id(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todoContainer WHERE id=?", (id,))
        data = cursor.fetchone()
        conn.close()
        return data
    def write_tb_todoContainer(self,text,user):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todoContainer (text,user) values (?,?)", (text,user))
        conn.commit()
        conn.close()
    def delete_tb_todoContainer(self,id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todoContainer WHERE id=?", (id,))
        conn.commit()
        conn.close()
    #table todo
    def read_tb_todo(self):
        conn =self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todo ")
        data_table = cursor.fetchall()
        conn.close()
        return data_table
    def write_tb_todo(self,comentar):
        conn =self.connect()
        cursor = conn.cursor()
        date = dt.datetime.now()#.strptime("%Y-%m-%dT%H:%M:")
        cursor.execute('''INSERT INTO todo (comentar, date) VALUES (?, ?)''', (comentar, date))
        conn.commit()
        conn.close()
