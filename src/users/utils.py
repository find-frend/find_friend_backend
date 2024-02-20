from io import BytesIO

from django.core.files import File
from PIL import Image


def make_thumbnail(image, size=(100, 100)):
    """Изменяет размер аватара на заданный размер."""
    im = Image.open(image)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    # im.convert("RGB")
    im.thumbnail(size)
    thumb_io = BytesIO()
    im.save(thumb_io, "JPEG", quality=85)
    return File(thumb_io, name=image.name)
