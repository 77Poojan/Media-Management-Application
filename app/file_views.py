import os

from app.forms import FileUploadForm
from app.models import FileUpload
from app.serializers.file_serializer import FileUploadSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES:
        files = request.FILES.getlist('file')  # Retrieve all uploaded files

        # Check if the number of files exceeds the limit
        if len(files) > 10:
            return JsonResponse({
                'success': False,
                'errors': ['You can upload a maximum of 10 files at a time.']
            }, status=400)

        error_messages = []
        successful_uploads = []

        for file in files:
            # Check if a file with the same name already exists
            file_name = file.name
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            if os.path.exists(file_path):
                successful_uploads.append(f"File '{file_name}' already exists, skipping upload.")
                continue  # Skip this file if it already exists

            # Create a new form instance for each file
            form = FileUploadForm(data=request.POST, files={'file': file})
            if form.is_valid():
                file_instance = form.save()
                successful_uploads.append(file_instance.file.name)  # Collect file names for reference
            else:
                error_messages.append(f"Error uploading file '{file.name}': {form.errors.get('file', ['Invalid file'])[0]}")

        # Check if there were any errors
        if error_messages:
            return JsonResponse({
                'success': False,
                'errors': error_messages
            }, status=400)

        # If all files were uploaded successfully
        return JsonResponse({
            'success': True,
            'message': f'{len(successful_uploads)} file(s) uploaded successfully!',
            'uploaded_files': successful_uploads
        })

    return JsonResponse({'success': False, 'error': 'No files uploaded.'}, status=400)


class FilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    
# Main file list API view using DRF pagination
@api_view(['GET'])
@csrf_exempt
def file_list(request):
    try:
        files = FileUpload.objects.all().order_by('-uploaded_at')
        paginator = FilePagination()
        paginator.page_size = 10 
        result_page = paginator.paginate_queryset(files, request)
        serializer = FileUploadSerializer(result_page, many=True)
        paginated_response = paginator.get_paginated_response(serializer.data)
        return paginated_response

    except FileUpload.DoesNotExist:
        return Response({'error': 'No files found.'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@csrf_exempt
def delete_file(request, file_id):
    if request.method == 'DELETE':
        try:
            # Retrieve the file instance by its ID
            file_instance = FileUpload.objects.get(id=file_id)
            
            # Construct the full path to the file in the media folder
            file_path = os.path.join(settings.MEDIA_ROOT, file_instance.file.name)

            # Check if the file exists and remove it from the file system
            if os.path.exists(file_path):
                os.remove(file_path)

            # Delete the file record from the database
            file_instance.delete()

            # Return a successful response
            return JsonResponse({
                'success': True,
                'message': f'File with ID {file_id} and its record have been deleted successfully.'
            })
        except FileUpload.DoesNotExist:
            # If the file record does not exist in the database
            return JsonResponse({
                'success': False,
                'error': f'File with ID {file_id} not found.'
            }, status=404)
        except Exception as e:
            # Handle any unexpected errors
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            }, status=500)
    
    # Handle invalid HTTP method (not DELETE)
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method. Only DELETE is allowed.'
    }, status=405)
