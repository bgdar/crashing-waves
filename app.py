from flask import Flask,flash,url_for,redirect,render_template,request,session,abort,jsonify,Response
import json
import sqlite3
from functools import wraps
import json
# import sub folder
from static.todouser.kelolaTodo import ManagemenFile as mf

#koneksi ke databases contact.db dgn file terpisah
from get_db import get_db

app = Flask(__name__)


app.config["BASE_URL"] ="secret_key"
app.secret_key="penetapan secret key"

@app.route('/', methods=['GET', 'POST'])
def dashboard():    
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        user = get_db().read_tb_users(name,password)
        if user :
            session['user'] = {'name': name, 'password': password} 
            return redirect(url_for('home'))
        elif not name or not password :
            flash('nama dan password harus diisi',"error")
        else:
           flash(f" username atas nama {name} tersebut tidak di temukan...","error")
    user_session = session.get('user')
    if not user_session or not user_session.get('name') or not user_session.get('password'):
        sesion = "null" 
    else:
        sesion = user_session.get('name')  

    data = {
        "session": json.dumps(sesion),
        }
    return render_template('users/dashboard.html',**data)
@app.route('/singin',methods=['GET','POST'])
def singin(): #pengelolaan singin baru dari user
    database = get_db()
    if request.method == 'POST':
        namesingin = request.form.get('namesingin')
        passwordsingin = request.form.get('passwordsingin')
        if namesingin and passwordsingin :# bila namesingin and passwordsingin tidak kosong (tunggu dulu)
            database.write_tb_users(namesingin, passwordsingin)
            textSuccess = f" data atas nama {namesingin} berhasil di tambahkan"
            return render_template('users/singin.html',textSuccess = textSuccess)
        else :
            textError = f" {namesingin} dan {passwordsingin} gagal di tambahkan"
            return render_template('users/singin.html',textError = textError)
    return render_template('users/singin.html')
    

def login_required(f): # Menggunakan dekorator untuk autentikasi adalah metode yang efisien dan terstruktur untuk memeriksa apakah pengguna telah login sebelum mengakses rute tertentu di aplikasi Flask Anda
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("login dulu mase","error")
            return redirect(url_for('dashboard'))  # Mengalihkan ke halaman login jika tidak ada sesi pengguna
        return f(*args, **kwargs)
    return decorated_function

@app.route('/home', methods=['GET'])
@login_required
def home():
    data = {
        "title": 'halaman HOme',
        "fileCss" : "home.css",
        "fileJs":"home.js"
    }
    return render_template('home.html',**data)
@app.route('/home/<string:logout>', methods=['POST'])
def homeLogout(logout):
    if logout:
        session.pop('user', None)
        flash("you successfully logged out",'success'),200
        return jsonify({"message":"User logout success"})
    print(logout)

@app.route('/about',methods=['GET'])
@login_required
def about():
    data = {
        "title": 'halaman About',
        "fileCss" : "about.css"
    }
    return render_template('about.html', **data)

# Router untuk Halaman contact
@app.route('/contact',methods=['GET', 'POST',])
@login_required
def contact():#Default Parameter: Ini memastikan bahwa jika route /contact diakses tanpa ID,
    data_contact = get_db().read_tb_contact() #baca semua data
    #tambah data conatct
    writeContact =""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        age = request.form.get('age')
        #all([name, email, phone, age]) akan mengembalikan True jika semua elemen dalam list tidak kosong atau False jika salah satu atau lebih elemen kosong atau None.
        if all([name, email, phone, age]): 
            get_db().write_tb_contact(name,email,phone,age)
            writeContact = f"Data atas nama {name} Berhasil di tambahkan silahkan relout halaman"
        else :
            writeContact = "Data gagal di tambahkan"

    data = {
        "const":1,
        "textAddContact":writeContact,
        "data_contact" : data_contact,
        "title": 'halaman Contact',
        "fileCss" : "contact.css",
        "fileJs": "contact.js"
    }
    return render_template('contacts/contact.html',**data)
@app.route('/contact/<int:id>',methods=['GET'])# pencarian contact berdasarka id
def contact_id(id):
    data_id= get_db().read_tb_contact_id(id) 
    if data_id is None:
        abort(404, description="Contact not found")
    return jsonify(data_id)
@app.route("/contact/update/<int:id>",methods=['GET','POST'])
def update_contact(id):
    dataID = get_db().read_tb_contact_id(id)
    if request.method == "POST":
        # Ambil data dari form
        form_data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "phone": request.form.get('phone'),
            "age": request.form.get('age')
        }
        print(form_data)
        print("all ",all(form_data.values()))
        # Cek jika semua field terisi
        if all(form_data.values()):
            # Proses update data
            isSame = (
                form_data["name"] == dataID[1] and 
                form_data["email"] == dataID[2] and
                form_data["phone"] == dataID[3] and 
                form_data['age'] == str(dataID[4]) #ada kemungkina data di form str
            )
            if isSame:
                flash("Data ini tidak perlu di update jika sama","error")
            else:
                get_db().update_tb_contact(
                    id,
                    form_data['name'], 
                    form_data['email'], 
                    form_data['phone'], 
                    form_data['age']
                )
                flash(f"Data atas nama {dataID[1]} berhasil diupdate dan back ke halaman update", "success")
                return render_template("contacts/contactUpdate.html", dataID=dataID)
        else:
            flash("Data gagal diupdate, pastikan semua field terisi", "error")
    return render_template("contacts/contactUpdate.html", dataID=dataID)

@app.route("/delete_contact",methods=["GET","POST", "DELETE",])
def delete_contact():
    try :  # Mengambil data JSON dari body permintaan
        request_data = request.get_json()
        data_id = request_data.get('id')
            # Validasi ID data
        if data_id:
                # Hapus data berdasarkan ID
            get_db().delete_tb_contact_id(data_id)
            return jsonify({"message": f"Data dengan id {data_id} berhasil dihapus"}), 200
        else:
            return jsonify({"error": "ID tidak ditemukan"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/todo',methods=["GET"])
def todo():
    #masukan contener text dan user dari db containetodo
    #dan tambahkan data create ke tabel Containerodo
    textContainer = get_db().read_tb_todoContainer()
    data = {
        "textContainer": textContainer,
        "title": 'halaman todo',
        "fileCss" : "todo.css",
        "fileJs": "todo.js"
    }
    
    return render_template('/todo/todo.html',**data)

@app.route('/todo/add', methods=['POST'])
def add_todo():
    data = request.get_json()
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type harus 'application/json'"}), 415  # 415 Unsupported Media Type
    if not data or 'todo' not in data:
        return jsonify({"error": "Data tidak valid"}), 400
    todo_contain = data['todo']
    user = session.get("user").get("name")
    print(todo_contain)
    if todo_contain :
        print(todo_contain)
        get_db().write_tb_todoContainer(user,todo_contain)  
    # Simpan data To-Do baru ini ke database atau daftar
    return jsonify({"status": "success", "todo": todo_contain}), 200
@app.route('/todo/delete/<int:id>', methods=['POST', 'DELETE'])
def delete_todo(id):
    if id:
        get_db().delete_tb_todoContainer(id)  # Ensure this function works as expected
        return jsonify({"status": "success", "id": id}), 200
    else:
        print("ID not found")
        return jsonify({"error": "Data tidak valid"}), 400
@app.route('/todo/todo-user/<id>', methods=['GET'])
def todo_user(id):
    print('id user yg di kirim :',id)
    user_data = get_db().read_tb_todoContainer_id(id)
    try:
        mf.read_file(user_data[0])
        print('file ditemukan')
    except Exception as e:
        print('file gagal ditemukan')
        print(e)

    data = {
        "user_data": user_data,
        "title": 'halaman todo user',
        "fileCss" : "todo-user.css",
        "fileJs" : "todo-user.js"
    }
    return render_template('/todo/todo-user.html',**data)

@app.route('/todo/todoSave', methods=['POST'])
def todoSave():
    request_data = request.get_json()
    data_todo = request_data.get('todo')
    nameFile = request_data.get('nameFile')
    print(f" data :{data_todo} name file : { nameFile}")

@app.route('/pesanLogin',methods=['GET']) #Halaman ini Akan muncul ketika token sesion belum ada 
def pesanLogin():
    return render_template("PesanLogin.html")

@app.errorhandler(404) # pengecekan untuk halaman yg tidak ditemukan 
def page_not_found(e):
    return render_template('error/404.html'), 404

if __name__ == "__main__": 
    app.run(debug=True,port=5007)
    