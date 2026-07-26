from datetime import datetime
from django.db import transaction
from .models import Rider
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile



@transaction.atomic
def generate_rider_id():
    year = datetime.now().year

    last_rider = (
        Rider.objects
        .select_for_update()
        .exclude(rider_id__isnull=True)
        .exclude(rider_id="")
        .filter(rider_id__startswith=f"SRITS-{year}-")
        .order_by("-rider_id")
        .first()
    )

    if last_rider:
        last_number = int(last_rider.rider_id.split("-")[-1])
        next_number = last_number + 1
    else:
        next_number = 1

    return f"SRITS-{year}-{next_number:06d}"


def generate_qr_code(rider):
    verification_url = f"https://srits.gov.ng/verify/{rider.rider_id}"

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(verification_url)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    image.save(buffer, format="PNG")

    filename = f"{rider.rider_id}.png"

    rider.qr_code.save(
        filename,
        ContentFile(buffer.getvalue()),
        save=False,
    )