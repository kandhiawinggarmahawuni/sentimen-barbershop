from django.db import models

class Ulasan(models.Model):
    teks = models.TextField()
    label = models.CharField(max_length=10, choices=[('positif', 'Positif'), ('negatif', 'Negatif')], blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)
    nama = models.CharField(max_length=100, blank=True, null=True)
    rating = models.CharField(max_length=20, blank=True, null=True)
    review_date = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=20, default='manual', choices=[('manual', 'Manual'), ('google', 'Google')])

    def __str__(self):
        return self.teks[:50]
