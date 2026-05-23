from typing import Any

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import pickle

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_super_aman'

with open('vektor_kata.pkl', 'rb') as f:
    vectorizer = pickle.load(f)
with open('model_ai.pkl', 'rb') as f:
    ai_model = pickle.load(f)
# ----------------------------

# --- FASE SETUP BRANKAS ---
def get_db_connection():
    conn = sqlite3.connect('database.db', timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Laci untuk akun login
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
            nama_pengirim TEXT,
            isi_pesan TEXT,
            label_pesan TEXT
        )
    ''')
    # Laci BARU untuk menyimpan daftar portofolio (Fitur CRUD)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT,
            deskripsi TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()
# ---------------------------

@app.route('/')
def halaman_utama():
    return render_template('index.html')

# --- RUTE PENGUNJUNG MENGIRIM PESAN ---
@app.route('/kirim_pesan', methods=['POST'])
def kirim_pesan():
    nama = request.form['nama']
    pesan = request.form['pesan']
    
    # [PELACAK 1] 
    print(f"\n[INFO] Menerima pesan dari: {nama}")
    
    # 1. AI Membaca dan Menebak Pesan
    pesan_angka = vectorizer.transform([pesan])
    tebakan_ai = ai_model.predict(pesan_angka)[0] 
    
    # 2. PENERJEMAH (SANGAT PENTING)
    # paksa dialek Numpy dari AI menjadi teks Python standar menggunakan str()
    kategori_final = str(tebakan_ai)
    
    # [PELACAK 2]
    print(f"[INFO] AI melabeli pesan ini sebagai: {kategori_final}\n")
    
    # 3. Simpan pesan beserta tebakan AI ke database
    conn = get_db_connection()
    conn.execute('INSERT INTO messages (nama_pengirim, isi_pesan, label_ai) VALUES (?, ?, ?)', (nama, pesan, kategori_final))
    conn.commit()
    conn.close()
    
    return redirect(url_for('halaman_utama'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_ketik = request.form['username']
        pass_ketik = request.form['password']
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user_ketik, pass_ketik))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Gagal: Username sudah terdaftar!"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_ketik = request.form['username']
        pass_ketik = request.form['password']
        
        conn = get_db_connection()
        akun = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (user_ketik, pass_ketik)).fetchone()
        conn.close()
        
        if akun:
            session['username'] = akun['username']
            return redirect(url_for('dashboard'))
        else:
            return "Login Gagal: Username atau Password salah!"
    return render_template('login.html')

# --- FITUR CRUD DI DASBOR ---

# READ: Menampilkan halaman dasbor beserta isi laci projects
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        conn = get_db_connection()
        
        # 1. Pelayan mengambil daftar proyek
        semua_proyek = conn.execute('SELECT * FROM projects').fetchall()
        
        # 2. BARU: Pelayan juga harus mengambil daftar pesan!
        semua_pesan = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
        
        conn.close()
        
        # 3. BARU: Pelayan membawa KEDUA data tersebut ke meja (dashboard.html)
        return render_template('dashboard.html', username=session['username'], daftar_proyek=semua_proyek, daftar_pesan=semua_pesan)
    
    return redirect(url_for('login'))


@app.route('/tambah_proyek', methods=['POST'])
def tambah_proyek():
    if 'username' in session:
        judul_baru = request.form['judul']
        deskripsi_baru = request.form['deskripsi']
        
        conn = get_db_connection()
        conn.execute('INSERT INTO projects (judul, deskripsi) VALUES (?, ?)', (judul_baru, deskripsi_baru))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))

# DELETE: Rute untuk menghapus proyek berdasarkan ID-nya
@app.route('/hapus_proyek/<int:id_proyek>')
def hapus_proyek(id_proyek):
    if 'username' in session:
        conn = get_db_connection()
        conn.execute('DELETE FROM projects WHERE id = ?', (id_proyek,))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
# DELETE: Rute untuk menghapus pesan dari kotak masuk
@app.route('/hapus_pesan/<int:id_pesan>')
def hapus_pesan(id_pesan):
    if 'username' in session:
        conn = get_db_connection()
        conn.execute('DELETE FROM messages WHERE id = ?', (id_pesan,))
        conn.commit()
        conn.close()
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    app.run(debug=True)
