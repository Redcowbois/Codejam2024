from django import forms
from django.core.validators import FileExtensionValidator

class UploadFileForm(forms.Form):
    file = forms.FileField(max_length=800000000)