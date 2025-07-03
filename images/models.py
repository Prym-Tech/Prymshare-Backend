import os
from django.db import models
from django.conf import settings
from PIL import Image as PILImage
from io import BytesIO
from django.core.files.base import ContentFile

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.owner.id}/{filename}'

class Image(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.owner.email} uploaded at {self.uploaded_at}"

    def save(self, *args, **kwargs):
        if self.image:
            # Open the uploaded image
            pil_img = PILImage.open(self.image)

            # Convert image to RGB if it's not
            if pil_img.mode != 'RGB':
                pil_img = pil_img.convert('RGB')

            # Create a file-like object to hold the compressed image data
            im_io = BytesIO() 

            # Save the image to the in-memory file, compressing it
            pil_img.save(im_io, 'JPEG', quality=70, optimize=True)

            # Create a new Django File object from the in-memory file
            new_image = ContentFile(im_io.getvalue(), name=self.image.name)

            self.image = new_image
            
        super().save(*args, **kwargs)

