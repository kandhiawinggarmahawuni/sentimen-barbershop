# analisis/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('predict/', views.predict_view, name='predict'),
    path('dataset/', views.dataset_view, name='dataset'),
    path('update-model/', views.update_model_view, name='update_model')
]
