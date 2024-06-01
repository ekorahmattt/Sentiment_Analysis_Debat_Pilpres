from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for
from nlp_function import clean_tweet, normalisasi, stopword, tokenizing, stemming, classification, csv_analize

app = Flask(__name__)

# Konfigurasi Koneksi ke Database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pilpres'

mysql = MySQL(app)

################################# HALAMAN INDEX #####################################################
@app.route('/')
def index():

    # Ambil data persentase sentiment setiap paslon
    cap = mysql.connection.cursor()
    cap.execute('SELECT * FROM capres')
    data = cap.fetchall()
    cap.close()

    return render_template('index.html', data=data)

################################# Halaman Analisis Uploaded File #####################################################
@app.route('/analisis', methods=['POST'])
def analisis():

    # Menangkap File yang di upload
    f = request.files['file']
    filename = f.filename

    # Proses Analisis File dengan Fungsi yang menghasilkan persentase positif, netral, dan negatif
    positif, netral, negatif, total, freq = csv_analize(f, filename)
    
    # Menyeleksi frekuensi kata-kata yang didapat dari file yang di upload
    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    freq = dict(freq[:10])
    
    return render_template('analisis.html',
                           positif=positif, 
                           netral=netral,
                           negatif=negatif,
                           total = total,
                           freq = freq,
                           filename=filename)

################################ Halaman Analisis Teks Tweet ######################################################
@app.route('/hasil', methods=['POST'])
def hasil():

    # Prosesing teks yang dikirim (data cleaning, normalisasi, menghapus stopword, tokenisasi, stemming)
    tweet = request.form['message']
    cleaned = clean_tweet(tweet)
    normal = normalisasi(cleaned)
    stopwrd = stopword(normal)
    tokenized = tokenizing(stopwrd)
    stemmed = stemming(tokenized)

    # Klasifikasi teks yang telah di prossesing
    resul, classify = classification(stemmed)

    return render_template('hasil.html', 
                           tweet=tweet,
                           cleaned=cleaned,
                           normal=normal,
                           stopwrd=stopwrd,
                           tokenized=tokenized,
                           stemmed=stemmed,
                           classify=classify,
                           resul = resul
                        )

############################## Halaman Capres dan Cawapres ###########################################################
@app.route('/paslon/<nomor>')
def paslon(nomor):
    
    capres = ['Anies Rasyid Baswedan','Prabowo Subianto','Ganjar Pranowo']
    cawapres = ['Muhaimin Iskandar','Gibran Rakabuming Raka','Mahfud MD']
    capa = capres[int(nomor)-1]
    cawa = cawapres[int(nomor)-1]
    
    # Memuat analisis dari file database yang berkaitan dengan paslon
    positif_capa, netral_capa, negatif_capa, total_capa, freq_capa = csv_analize("dataset/"+capa+".csv", "capres", capa)
    positif_cawa, netral_cawa, negatif_cawa, total_cawa, freq_cawa = csv_analize("dataset/"+cawa+".csv", "cawapres", cawa)

    # Menghitung akumulasi persentase sentiment capres dan cawapres
    positif_paslon =  round(((positif_capa/100 * total_capa)+(positif_cawa/100 * total_cawa))/(total_capa + total_cawa) * 100)
    netral_paslon =  round(((netral_capa/100 * total_capa)+(netral_cawa/100 * total_cawa))/(total_capa + total_cawa) * 100)
    negatif_paslon =  round(((negatif_capa/100 * total_capa)+(negatif_cawa/100 * total_cawa))/(total_capa + total_cawa) * 100)
    
    # Menyimpan hasil akumulasi
    cur = mysql.connection.cursor()
    cur.execute('''UPDATE capres SET positif=%s, netral=%s, negatif=%s WHERE paslon=%s ''', (positif_paslon,netral_paslon,negatif_paslon,capa))
    mysql.connection.commit()

    # Menyeleksi frekuensi kata-kata yang terdapat pada data sentiment
    freq_capa = sorted(freq_capa.items(), key=lambda x:x[1], reverse=True)
    freq_capa = dict(freq_capa[:10])
    freq_cawa = sorted(freq_cawa.items(), key=lambda x:x[1], reverse=True)
    freq_cawa = dict(freq_cawa[:10])

    return render_template('paslon.html', 
                           capa=capa, 
                           cawa=cawa,
                           positif_capa=positif_capa,
                           netral_capa=netral_capa,
                           negatif_capa=negatif_capa,
                           total_capa=total_capa,
                           freq_capa=freq_capa,
                           positif_cawa=positif_cawa,
                           netral_cawa=netral_cawa,
                           negatif_cawa=negatif_cawa,
                           total_cawa=total_cawa,
                           freq_cawa=freq_cawa,
                           positif_paslon=positif_paslon)

########################################## RUNNING PROGRAM ###################################################
if __name__ == "__main__":
    app.run(debug=True)