import magic
from django.db import models
from core.mixins import TimeStampModel
from django.contrib.auth.models import AbstractUser
from core.validators import validate_image_audio_video


# User Model
class User(AbstractUser, TimeStampModel):
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False)
    email_verified = models.BooleanField(default=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  
        blank=True,
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Custom related name
        blank=True,
    )
    
    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.email
    
    
# Abstract Base Class for File Uploads and Downloads
class AbstractFile(models.Model):
    file = models.FileField(upload_to='uploads/', validators=[validate_image_audio_video])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=10, 
        choices=[('image', 'Image'), ('audio', 'Audio'), ('video', 'Video'), ], 
        null=True, blank=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.file.name

    @property
    def file_size(self):
        return self.file.size

    @property
    def file_name(self):
        return self.file.name

    @property
    def file_type(self):
        """
        Determine file type based on MIME type using `magic` library.
        """
        mime_type = magic.from_buffer(self.file.read(), mime=True)
        self.file.seek(0)  # Reset file pointer to the beginning
        return mime_type

    def get_category_from_mime_type(self):
        """
        Returns the category based on the MIME type.
        """
        mime_type = self.file_type
        if 'audio' in mime_type:
            return 'audio'
        elif 'video' in mime_type:
            return 'video'
        elif 'image' in mime_type:
            return 'image'
        return 'other'

    def save(self, *args, **kwargs):
        """
        Overriding save method to set the file category before saving.
        """
        if not self.category:
            self.category = self.get_category_from_mime_type()
        super().save(*args, **kwargs)


# Upload File Model
class FileUpload(AbstractFile):
    pass


#  Download File Model
class FileDownload(AbstractFile):
    pass
