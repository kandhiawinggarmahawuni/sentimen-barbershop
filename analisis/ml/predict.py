import os
import joblib
from .preprocess import preprocess_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, './model-ml/naivebayes_model.pkl'))
vectorizer = joblib.load(os.path.join(BASE_DIR, './model-ml/vectorizer.pkl'))

def predict_sentiment(text):
    clean_text = preprocess_text(text)
    vec = vectorizer.transform([clean_text])
    pred = model.predict(vec)
    return pred[0]