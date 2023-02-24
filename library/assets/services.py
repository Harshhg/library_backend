import base64
from library.assets.models import Image


def save_verification_id(verification_id):
    name = verification_id.name
    data = verification_id.read()
    encoded_string = base64.b64encode(data)
    image = Image(name=name, data=encoded_string)
    image.save()
    return image
