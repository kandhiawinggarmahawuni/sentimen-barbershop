"""
Modul ini digunakan untuk melatih model pembelajaran mesin untuk analisis sentimen
dan menyimpannya ke dalam file agar dapat digunakan untuk prediksi di masa mendatang.

Library yang digunakan:
1. os:
   - Digunakan untuk menangani operasi terkait sistem file, seperti menentukan lokasi penyimpanan model.
2. joblib:
   - Digunakan untuk menyimpan model pembelajaran mesin dan vectorizer dalam format `.pkl`.
3. sklearn.feature_extraction.text.TfidfVectorizer:
   - Digunakan untuk mengubah teks menjadi representasi numerik menggunakan metode TF-IDF.
4. sklearn.naive_bayes.MultinomialNB:
   - Algoritma Naïve Bayes yang digunakan untuk melatih model klasifikasi sentimen.
5. imblearn.over_sampling.RandomOverSampler:
   - Digunakan untuk menangani ketidakseimbangan data dengan melakukan oversampling pada kelas minoritas.
6. preprocess_text (dari modul preprocess):
   - Fungsi untuk membersihkan dan memproses teks sebelum digunakan untuk pelatihan model.
7. analisis.models.Ulasan:
   - Model Django yang digunakan untuk mengambil data ulasan dari database.

Fungsi utama:
1. train_and_save_model_from_db():
   - Mengambil data ulasan dari database, memproses teks, melatih model Naïve Bayes,
     dan menyimpan model serta vectorizer ke dalam file.

Langkah-langkah dalam fungsi:
1. Mengambil data ulasan dari database yang memiliki label (tidak null).
2. Membersihkan teks ulasan menggunakan fungsi `preprocess_text`.
3. Mengubah teks menjadi representasi numerik menggunakan TF-IDF Vectorizer.
4. Menangani ketidakseimbangan data dengan RandomOverSampler.
5. Melatih model Naïve Bayes menggunakan data yang telah di-resample.
6. Menyimpan model dan vectorizer ke dalam file `.pkl` untuk digunakan di masa mendatang.

Error Handling:
- Jika tidak ada data ulasan yang tersedia untuk pelatihan, fungsi akan mengembalikan error `ValueError`.

File yang dihasilkan:
1. `naivebayes_model.pkl`: Model Naïve Bayes yang telah dilatih.
2. `vectorizer.pkl`: TF-IDF Vectorizer yang telah dilatih.

Contoh Penggunaan:
Fungsi ini biasanya dijalankan untuk memperbarui model berdasarkan data ulasan terbaru di database.
"""

import os

import joblib
from imblearn.over_sampling import RandomOverSampler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from analisis.models import Ulasan

from .preprocess import preprocess_text


def train_and_save_model_from_db():
    # Ambil data dari DB
    queryset = Ulasan.objects.exclude(label__isnull=True)
    texts = [preprocess_text(obj.teks) for obj in queryset]
    labels = [obj.label for obj in queryset]

    if not texts:
        raise ValueError("Tidak ada data ulasan yang bisa digunakan untuk training.")

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    y = labels

    # Oversampling
    oversampler = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = oversampler.fit_resample(X, y)

    # Training model Naïve Bayes
    model = MultinomialNB()
    model.fit(X_resampled, y_resampled)

    # Simpan model & vectorizer
    base_path = os.path.dirname(__file__)
    joblib.dump(model, os.path.join(base_path, "model-ml/naivebayes_model.pkl"))
    joblib.dump(vectorizer, os.path.join(base_path, "model-ml/vectorizer.pkl"))
