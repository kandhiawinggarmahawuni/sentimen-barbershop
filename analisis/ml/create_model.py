# create-model.py
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from imblearn.over_sampling import RandomOverSampler

from .preprocess import preprocess_text
from analisis.models import Ulasan

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
    joblib.dump(model, os.path.join(base_path, 'model-ml/naivebayes_model.pkl'))
    joblib.dump(vectorizer, os.path.join(base_path, 'model-ml/vectorizer.pkl'))
