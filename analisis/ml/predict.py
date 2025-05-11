"""
Modul ini digunakan untuk memprediksi sentimen dari teks ulasan menggunakan model pembelajaran mesin.

Library yang digunakan:
1. os:
   - Digunakan untuk menangani operasi terkait sistem file, seperti mendapatkan direktori file saat ini.
2. joblib:
   - Digunakan untuk memuat model pembelajaran mesin dan vectorizer yang telah disimpan dalam format `.pkl`.
3. preprocess_text (dari modul preprocess):
   - Fungsi ini digunakan untuk membersihkan dan memproses teks sebelum dilakukan prediksi.

Fungsi utama:
1. predict_sentiment(text):
   - Memprediksi sentimen dari teks ulasan yang diberikan.
   - Sentimen diprediksi menggunakan model Naive Bayes yang telah dilatih sebelumnya.
   - Mengembalikan hasil prediksi berupa label sentimen (misalnya, "positif" atau "negatif").
"""

import os

import joblib

from .preprocess import preprocess_text

# Mendapatkan direktori file saat ini
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Memuat model Naive Bayes yang telah dilatih
model = joblib.load(os.path.join(BASE_DIR, "./model-ml/naivebayes_model.pkl"))

# Memuat vectorizer untuk mengubah teks menjadi representasi numerik
vectorizer = joblib.load(os.path.join(BASE_DIR, "./model-ml/vectorizer.pkl"))


def predict_sentiment(text):
    """
    Memprediksi sentimen dari teks ulasan yang diberikan.

    Parameter:
    - text (str): Teks ulasan yang akan diprediksi.

    Langkah-langkah:
    1. Memeriksa apakah teks kosong. Jika kosong, akan mengembalikan error.
    2. Membersihkan teks menggunakan fungsi preprocess_text.
    3. Mengubah teks yang telah dibersihkan menjadi representasi numerik menggunakan vectorizer.
    4. Melakukan prediksi sentimen menggunakan model Naive Bayes.
    5. Mengembalikan hasil prediksi berupa label sentimen.

    Return:
    - str: Label sentimen (misalnya, "positif" atau "negatif").
           Jika terjadi error, akan mengembalikan pesan error.

    Error Handling:
    - ValueError: Jika teks kosong.
    - Exception: Jika terjadi error lain selama proses prediksi.

    Contoh:
    >>> predict_sentiment("Produk ini sangat bagus!")
    'positif'
    """
    try:
        if not text or not text.strip():
            raise ValueError("Teks ulasan kosong.")

        # Membersihkan teks ulasan
        clean_text = preprocess_text(text)

        # Mengubah teks menjadi representasi numerik
        vec = vectorizer.transform([clean_text])

        # Melakukan prediksi sentimen
        pred = model.predict(vec)
        print(f"[predict_sentiment] Hasil prediksi: {pred}")
        return pred[0]

    except ValueError as ve:
        print(f"[predict_sentiment] Input error: {ve}")
        return "error: input kosong"

    except Exception as e:
        print(f"[predict_sentiment] Terjadi error saat prediksi: {e}")
        return "error: gagal prediksi"
