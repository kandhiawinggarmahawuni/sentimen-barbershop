from django import forms
from .models import Ulasan

class UlasanForm(forms.ModelForm):
    class Meta:
        model = Ulasan
        fields = ['teks', 'label']
        widgets = {
            'teks': forms.Textarea(attrs={'class': 'border rounded p-2 w-full', 'rows': 3}),
            'label': forms.Select(attrs={'class': 'border rounded p-2 w-full'})
        }

class CSVUploadForm(forms.Form):
    file = forms.FileField()