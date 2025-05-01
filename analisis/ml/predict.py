import os
import joblib
from .preprocess import preprocess_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, './model-ml/naivebayes_model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, './model-ml/vectorizer.pkl'))

def predict_sentiment(text):
    try:
        if not text or not text.strip():
            raise ValueError("Teks ulasan kosong.")

        clean_text = preprocess_text(text)
        vec = vectorizer.transform([clean_text])
        pred = model.predict(vec)
        print(f"[predict_sentiment] Hasil prediksi: {pred}")
        return pred[0]

    except ValueError as ve:
        print(f"[predict_sentiment] Input error: {ve}")
        return "error: input kosong"

    except Exception as e:
        print(f"[predict_sentiment] Terjadi error saat prediksi: {e}")
        return "error: gagal prediksi"
