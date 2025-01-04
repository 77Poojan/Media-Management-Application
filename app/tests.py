from django.test import TestCase

# Create your tests here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import FileUpload

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the file to the database
            form.save()
            return HttpResponse('File uploaded successfully!')
        else:
            return HttpResponse('Invalid file type or size.', status=400)
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})


from django.http import FileResponse, Http404
from .models import FileUpload
import os

def download_file(request, file_id):
    try:
        # Get the file object by ID
        file_upload = FileUpload.objects.get(id=file_id)
        
        # Open the file and return it as a download
        file_path = file_upload.file.path  # Path to the file
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_upload.file.name)
        else:
            raise Http404('File not found')
    except FileUpload.DoesNotExist:
        raise Http404('File not found')

def file_list(request):
    files = FileUpload.objects.all()  # Fetch all uploaded files
    return render(request, 'file_list.html', {'files': files})
