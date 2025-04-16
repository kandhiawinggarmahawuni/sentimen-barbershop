from django.db import models

class Ulasan(models.Model):
    teks = models.TextField()
    label = models.CharField(max_length=10, choices=[('positif', 'Positif'), ('negatif', 'Negatif')], blank=True)
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.teks[:50]
