"""
Modul ini digunakan untuk melakukan preprocessing teks sebelum digunakan dalam analisis sentimen
atau pelatihan model pembelajaran mesin.

Library yang digunakan:
1. string:
   - Digunakan untuk menghapus tanda baca dari teks.
2. re (Regular Expression):
   - Digunakan untuk menghapus angka dari teks.
3. Sastrawi.Stemmer.StemmerFactory:
   - Digunakan untuk melakukan stemming (mengubah kata ke bentuk dasar) pada teks berbahasa Indonesia.
4. Sastrawi.StopWordRemover.StopWordRemoverFactory:
   - Digunakan untuk menghapus kata-kata umum (stopwords) dalam bahasa Indonesia yang tidak memiliki makna signifikan.

Variabel Global:
1. stemmer:
   - Objek stemmer yang dibuat menggunakan `StemmerFactory` untuk melakukan stemming pada teks.
2. stopwords:
   - Daftar kata-kata umum (stopwords) dalam bahasa Indonesia yang akan dihapus dari teks.

Fungsi Utama:
1. preprocess_text(text):
   - Melakukan preprocessing pada teks yang diberikan.
   - Langkah-langkah preprocessing:
     a. Mengubah teks menjadi huruf kecil.
     b. Menghapus angka dari teks.
     c. Menghapus tanda baca dari teks.
     d. Menghapus spasi berlebih di awal dan akhir teks.
     e. Memisahkan teks menjadi kata-kata.
     f. Menghapus kata-kata yang termasuk dalam daftar stopwords.
     g. Melakukan stemming pada setiap kata untuk mengubahnya ke bentuk dasar.
   - Mengembalikan teks yang telah diproses sebagai string.

Parameter:
- text (str): Teks yang akan diproses.

Return:
- str: Teks yang telah diproses.
"""

import re
import string

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import \
    StopWordRemoverFactory

stemmer = StemmerFactory().create_stemmer()
stopwords = StopWordRemoverFactory().get_stop_words()


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"\d+", "", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.strip()
    words = text.split()
    filtered = [w for w in words if w not in stopwords]
    stemmed = [stemmer.stem(w) for w in filtered]
    return " ".join(stemmed)
