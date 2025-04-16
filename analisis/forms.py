from django import forms
from .models import Ulasan

class UlasanForm(forms.ModelForm):
    class Meta:
        model = Ulasan
        fields = ['teks']
        widgets = {
            'teks': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Masukkan ulasan'})
        }

class CSVUploadForm(forms.Form):
    file = forms.FileField()