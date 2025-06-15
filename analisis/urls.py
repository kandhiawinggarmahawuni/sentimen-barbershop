# analisis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('predict/', views.predict_view, name='predict'),
    path('dataset/', views.dataset_view, name='dataset'),
    path('update-model/', views.update_model_view, name='update_model'),
    path('sync-reviews/', views.sync_google_reviews, name='sync_reviews'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('delete-all-reviews/', views.delete_all_reviews, name='delete_all_reviews'),
]
