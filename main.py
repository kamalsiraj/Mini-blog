from flask import Flask, render_template, request, redirect, session
import json
import random
import time

app = Flask(__name__)
app.secret_key = "secretkey"  # Dibutuhkan untuk menggunakan session

# Fungsi untuk memuat soal dari file JSON
def load_soal():
    with open('soal.json', 'r') as file:
        return json.load(file)

@app.route('/')
def index():
    # Reset sesi jika kembali ke halaman utama
    session.clear()
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    soal_list = load_soal()

    # Cek apakah sesi sudah ada
    if 'waktu_mulai' not in session:
        # Inisialisasi sesi
        session['waktu_mulai'] = time.time()  # Waktu mulai kuis
        session['soal_terjawab'] = 0  # Hitung soal yang sudah dijawab
        session['soal_acak'] = random.sample(soal_list, len(soal_list))  # Soal diacak

    waktu_sekarang = time.time()
    soal_terjawab = session['soal_terjawab']
    soal_acak = session['soal_acak']

    # Batas waktu untuk soal saat ini (1 menit per soal)
    batas_waktu = session['waktu_mulai'] + (soal_terjawab + 1) * 60

    if request.method == 'POST':
        jawaban_user = request.form['jawaban']
        soal_id = int(request.form['soal_id'])
        soal = next((s for s in soal_acak if s["id"] == soal_id), None)

        if waktu_sekarang > batas_waktu:
            # Jika waktu habis, arahkan ke soal berikutnya
            session['soal_terjawab'] += 1
            return redirect('/quiz')  # Soal berikutnya

        if soal and jawaban_user.strip() == str(soal["jawaban"]):
            # Jika jawaban benar, lanjutkan ke soal berikutnya
            session['soal_terjawab'] += 1
            return render_template('result.html', hasil="Jawaban Benar! Lanjut ke soal berikutnya.")

        else:
            # Jika jawaban salah, arahkan ke soal berikutnya
            session['soal_terjawab'] += 1
            return render_template('result.html', hasil="Jawaban Salah! Coba Lagi.")

    # Cek apakah masih ada soal
    if soal_terjawab >= len(soal_acak):
        return render_template('result.html', hasil="Kuis selesai! Anda telah menjawab semua soal.")

    # Pilih soal berikutnya
    soal = soal_acak[soal_terjawab]
    waktu_tersisa = int(batas_waktu - waktu_sekarang)

    if waktu_tersisa <= 0:
        # Jika waktu habis, arahkan ke soal berikutnya
        session['soal_terjawab'] += 1
        return redirect('/quiz')  # Soal berikutnya

    return render_template('quiz.html', soal=soal, waktu_tersisa=waktu_tersisa)

if __name__ == '__main__':
    app.run(debug=True)
