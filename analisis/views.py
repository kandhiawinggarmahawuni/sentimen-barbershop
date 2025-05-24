from django.shortcuts import render, redirect
from django.contrib import messages
from analisis.models import Ulasan
from analisis.forms import UlasanForm, CSVUploadForm
from analisis.ml.predict import predict_sentiment, vectorizer, evaluate_model_from_file
from analisis.ml.create_model import train_and_save_model_from_db
import csv


# Dashboard view
def dashboard(request):
    # Data untuk kartu
    jumlah_total = Ulasan.objects.count()
    jumlah_positif = Ulasan.objects.filter(label='positif').count()
    jumlah_negatif = Ulasan.objects.filter(label='negatif').count()

    # Data untuk chart
    chart_labels = ['Positif', 'Negatif']
    chart_data = [
        jumlah_positif,
        jumlah_negatif,
    ]
    eval_result = evaluate_model_from_file()

    return render(request, 'analisis/dashboard.html', {
        'jumlah_total': jumlah_total,
        'jumlah_positif': jumlah_positif,
        'jumlah_negatif': jumlah_negatif,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'eval_result': eval_result,
    })


# Predict view
def predict_view(request):
    hasil = None
    if request.method == 'POST':
        form = UlasanForm(request.POST)
        if form.is_valid():
            teks = form.cleaned_data['teks']
            hasil = predict_sentiment(teks)
    else:
        form = UlasanForm()
    return render(request, 'analisis/predict.html', {'form': form, 'hasil': hasil})


# views.py
def dataset_view(request):
    ulasan_all = Ulasan.objects.all().order_by('-tanggal')
    ulasan_form = UlasanForm()
    csv_form = CSVUploadForm()

    if request.method == 'POST':
        if 'submit_manual' in request.POST:
            ulasan_form = UlasanForm(request.POST)
            if ulasan_form.is_valid():
                ulasan_form.save()
                return redirect('dataset')

        elif 'submit_csv' in request.POST:
            csv_form = CSVUploadForm(request.POST, request.FILES)
            if csv_form.is_valid():
                file = request.FILES['file']
                decoded = file.read().decode('utf-8').splitlines()
                reader = csv.reader(decoded)
                next(reader)  # skip header
                for row in reader:
                    Ulasan.objects.create(teks=row[0], label=row[1])
                return redirect('dataset')

    return render(request, 'analisis/dataset.html', {
        'data': ulasan_all,
        'ulasan_form': ulasan_form,
        'csv_form': csv_form,
    })


def update_model_view(request):
    try:
        train_and_save_model_from_db()  # <-- tidak perlu argumen
        messages.success(request, "Model berhasil di-train ulang dari database dan disimpan.")
    except Exception as e:
        messages.error(request, f"Gagal update model: {str(e)}")
    return redirect('dataset')
