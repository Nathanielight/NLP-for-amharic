from django import forms
from .models import AnalyzedDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = AnalyzedDocument
        fields = ['title', 'document', 'document_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),
        } 