"""
Modul ini digunakan untuk memprediksi sentimen dari teks ulasan menggunakan model pembelajaran mesin,
serta melakukan evaluasi model (akurasi, presisi, recall, f1-score) pada data uji.

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
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from .preprocess import preprocess_text
from analisis.ml.utils import to_percentage

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
        return pred[0]

    except Exception as e:
        print(f"[predict_sentiment] Terjadi error saat prediksi: {e}")
        return "error"


def evaluate_model_from_file():
    """
    Memuat data uji dari file dan melakukan evaluasi model (khusus label positif).
    Return:
        dict: {'akurasi': ..., 'presisi': ..., 'recall': ..., 'f1': ...}
    """
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        X_test_vec, y_test = joblib.load(
            os.path.join(base_path, "model-ml/test_data.pkl")
        )
        y_pred = model.predict(X_test_vec)

        # Hitung akurasi (tetap sama)
        akurasi = accuracy_score(y_test, y_pred)

        # Fokus ke label "positif" sesuai label dataset
        presisi = precision_score(y_test, y_pred, pos_label="positif", zero_division=0)
        recall = recall_score(y_test, y_pred, pos_label="positif", zero_division=0)
        f1 = f1_score(y_test, y_pred, pos_label="positif", zero_division=0)

        akurasi_persen = to_percentage(akurasi)
        presisi_persen = to_percentage(presisi)
        recall_persen = to_percentage(recall)
        f1_persen = to_percentage(f1)

        # logger evaluasi
        print(f"akurasi : {akurasi_persen}")
        print(f"presisi : {presisi_persen}")
        print(f"recall : {recall_persen}")
        print(f"f1 : {f1_persen}")

        return {
            "akurasi": akurasi_persen,
            "presisi": presisi_persen,
            "recall": recall_persen,
            "f1": f1_persen,
        }
    except Exception as e:
        print(f"[evaluate_model_from_file] Terjadi error saat evaluasi: {e}")
        return {"akurasi": "-", "presisi": "-", "recall": "-", "f1": "-"}
