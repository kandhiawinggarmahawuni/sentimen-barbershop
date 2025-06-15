from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from analisis.models import Ulasan
from analisis.forms import UlasanForm, CSVUploadForm
from analisis.ml.predict import predict_sentiment, vectorizer, evaluate_model_from_file
from analisis.ml.create_model import train_and_save_model_from_db
from analisis.ml.scrape_google_reviews import scrape_google_reviews
import csv
import json


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


def sync_google_reviews(request):
    if request.method == 'POST':
        try:
            # Get reviews from Google
            PLACE_REVIEW_URL = "https://maps.app.goo.gl/JAYDZXsL4wGNSYgC6?g_st=iw"
            reviews = scrape_google_reviews(PLACE_REVIEW_URL)
            
            # Track statistics
            added_count = 0
            skipped_count = 0
            
            # Process each review
            for review in reviews:
                # Check if review already exists
                if not Ulasan.objects.filter(
                    teks=review['review'],
                    nama=review['name'],
                    rating=review['rating'],
                    review_date=review['date']
                ).exists():
                    # Predict sentiment
                    sentiment = predict_sentiment(review['review'])
                    
                    # Skip if prediction failed
                    if sentiment == "error":
                        continue
                    
                    # Create new review with predicted sentiment
                    Ulasan.objects.create(
                        teks=review['review'],
                        nama=review['name'],
                        rating=review['rating'],
                        review_date=review['date'],
                        source='google',
                        label=sentiment  # sentiment is already a string
                    )
                    added_count += 1
                else:
                    skipped_count += 1
            
            return JsonResponse({
                'status': 'success',
                'message': f'Berhasil menambahkan {added_count} ulasan baru. {skipped_count} ulasan dilewati karena sudah ada.',
                'added': added_count,
                'skipped': skipped_count
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Gagal sync ulasan: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = Ulasan.objects.get(id=review_id)
            review.delete()
            return JsonResponse({
                'status': 'success',
                'message': 'Ulasan berhasil dihapus'
            })
        except Ulasan.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Ulasan tidak ditemukan'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Gagal menghapus ulasan: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)


def delete_all_reviews(request):
    if request.method == 'POST':
        try:
            count = Ulasan.objects.count()
            Ulasan.objects.all().delete()
            return JsonResponse({
                'status': 'success',
                'message': f'Berhasil menghapus {count} ulasan'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Gagal menghapus ulasan: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
