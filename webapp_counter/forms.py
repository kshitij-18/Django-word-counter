from django import forms
from .models import URLModel


class URLForm(forms.ModelForm):
    class Meta:
        model = URLModel
        fields = ('url',)
