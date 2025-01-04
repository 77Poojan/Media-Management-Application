from django.urls import path
from app.user_views import (
    UserRegisterView,
    UserListView,
    UserDetailView,
    UserLogoutView,
)
from app.file_views import (
    upload_file, 
    file_list,
    delete_file
)

urlpatterns = [
    # User-related URLS
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('<uuid:uuid>/', UserDetailView.as_view(), name='user-detail'),
    
    # File-related URLS
    path('upload/', upload_file, name='upload_file'),
    path('file-list/', file_list, name='file_list'),  
    path('delete-file/<int:file_id>/', delete_file, name='delete_file'),
]
