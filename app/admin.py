from django.contrib import admin
from app.models import User, FileUpload, FileDownload

# Register your models here.
admin.register(User)

@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_size', 'category', 'uploaded_at')

@admin.register(FileDownload)
class FileDownloadAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'file_size', 'category', 'uploaded_at')