from django.core.files.uploadedfile import SimpleUploadedFile
from pprint import pprint
import io
from PIL import Image
from accounts.models import Account


def object_to_dict(obj):
    if isinstance(obj, list):
        result = [object_to_dict(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        result = {key: object_to_dict(value) for key, value in obj.__dict__.items()}
    else:
        result = obj

    return result


def print_object(obj):
    pprint(object_to_dict(obj), indent=1)


def create_active_user(**kwargs):
    user = Account.objects.create_user(**kwargs)
    user.is_active = True
    user.save()
    return user


def create_test_image(name):
    buffer = io.BytesIO()
    image = Image.new("RGB", (100, 100), color="red")
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.read(), content_type="image/png")
