from pprint import pprint
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
