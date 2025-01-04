from rest_framework import serializers
from app.models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = FileUpload
        fields = ['id', 'file_name', 'file_size', 'file_type', 'category', 'uploaded_at', 'download_url']
    
    # Custom validation for the file upload
    def validate_file(self, value):
        # Add custom validations, like checking the file type
        return value

    # Method to generate the download URL
    def get_download_url(self, obj):
        # Assuming that the `file` field is a `FileField` in your model
        return obj.file.url  # Generate the URL for the file