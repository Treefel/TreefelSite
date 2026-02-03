import uuid
from io import BytesIO
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


def optimize_image(file_obj, max_dimension=1920, quality=85):
    """Resize and compress an image. Returns a BytesIO with JPEG data."""
    img = Image.open(file_obj)
    img = img.convert("RGB")

    if max(img.size) > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    output = BytesIO()
    img.save(output, format="JPEG", quality=quality, optimize=True)
    output.seek(0)
    return output


def upload_image(file_obj, folder="uploads"):
    """Optimize and upload an image to storage. Returns the URL."""
    optimized = optimize_image(file_obj)
    filename = f"{folder}/{uuid.uuid4().hex}.jpg"
    path = default_storage.save(filename, ContentFile(optimized.read()))
    return default_storage.url(path)
