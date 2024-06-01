import re
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from normalize_words import norm
from translate import Translator
from textblob import TextBlob
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary

# Klasifikasi menggunakan model Naive Bayes
loaded_model = pickle.load(open("models/NBPilpres_baru.pickle","rb"))
def classification(tweet):
    result = TextBlob(tweet, classifier=loaded_model)
    return result.polarity, result.classify()

################################### Menghapus Stopwords ##########################################################
stop_words = StopWordRemoverFactory().get_stop_words()
# stop_words.extend(more_stop_words)
new_array = ArrayDictionary(stop_words)
stop_words_remover_new = StopWordRemover(new_array)

def stopword(str_text):
    str_text = stop_words_remover_new.remove(str_text)
    return str_text

#################################### Membersihkan teks tweeter ###################################################
def clean_tweet(text):
    text = re.sub(r'@[A-Za-z0-9_]+', ' ', text) # Hapus @
    text = re.sub(r'#\w+','', text)             # Hapus #
    text = re.sub(r'RT[\s]+', '', text)         # Hapus Retweet
    text = re.sub(r'https?://\S+', '', text)    # Hapus hyperlink
    text = re.sub(r'[^A-Za-z0-9 ]', ' ', text)  # Hapus karakter kecuali abjad dan angka
    text = re.sub(r'\s+', ' ', text).strip()    # Hapus spasi berlebih
    text = text.lower()                         # Mengubah seluruh huruf menjadi kecil / lowercase
    return text

#################################### Normalisasi kata pada teks tweeter #########################################
def normalisasi(str_text):
    for i in norm:
        str_text = str_text.replace(i, norm[i]) # Mengganti kata yang terdapat di list norm
    return str_text

#################################### Tokenisasi ################################################################
def tokenizing(str_text):
    return ([i for i in str_text.split()]) # Memisahkan kata per kata

##################################### Stemming Teks ############################################################
def stemming(text_cleaning):
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    do = []
    for w in text_cleaning:
        dt = stemmer.stem(w)
        do.append(dt)
    d_clean = []
    d_clean = " ".join(do)
    return d_clean

def convert_eng(tweet):
    translator = Translator(to_lang="en", from_lang="id")
    translation = translator.translate(tweet)
    return translation

###################################### Analisis File Upload ####################################################
def csv_analize(files, filename="default", paslon="default"):
    
    # Ambil data dari file csv yang di upload menjadi dataframe
    df = pd.read_csv(files)
    total = df.shape[0]
    data_tweet = list(df['tweet_english'])
    kata = list(df['full_text'])
    polaritas = 0

    status = []
    freq = {}
    total_positif = total_negatif = total_netral = total = 0

    # Proses klasifikasi sentiment dari dataframe
    for i, tweet in enumerate(data_tweet):
        analysis = TextBlob(tweet)
        polaritas += analysis.polarity

        if analysis.sentiment.polarity > 0.0:
            total_positif += 1
            status.append('Positif')
        elif analysis.sentiment.polarity == 0.0:
            total_netral += 1
            status.append('Netral')
        else:
            total_negatif += 1
            status.append('Negatif')

        total += 1

    # Menghitung frekuensi kata yang muncul
    for content in kata:
        content_list = content.split()
        for word in content_list:
            if word not in freq:
                freq[word] = 1
            else:
                freq[word] += 1

    # Menggambar Wordcloud
    cloud = WordCloud(background_color='white').generate_from_frequencies(freq)
    plt.figure(figsize=(20, 10), facecolor=None)
    plt.imshow(cloud)
    plt.axis('off')
    plt.tight_layout(pad=0)
    if paslon != "default":
        plt.savefig('static/wordcloud/'+paslon+'.png')
    else:
        plt.savefig('static/wordcloud/wordcloud.png')

    # Menyimpan dataframe menjadi file baru
    df['sentimen'] = status
    df.to_csv('dataset/'+filename)

    # Akumulasi persentase sentiment yang dianalisis
    persen_positif = float("{:.2f}".format(total_positif/total * 100))
    persen_netral = float("{:.2f}".format(total_netral/total * 100))
    persen_negatif = float("{:.2f}".format(total_negatif/total * 100))

    return persen_positif, persen_netral, persen_negatif, total, freq
