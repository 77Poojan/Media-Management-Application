from django import forms
from app.models import FileUpload
from core.validators import validate_image_audio_video  # Your custom validator


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']  # Include the file field in the form

    def clean_file(self):
        file = self.cleaned_data['file']
        validate_image_audio_video(file)  # Validate using the custom validator
        return file
