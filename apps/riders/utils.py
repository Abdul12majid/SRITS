from datetime import datetime

from .models import Rider


def generate_rider_id():
    year = datetime.now().year

    last_rider = (
        Rider.objects.exclude(rider_id__isnull=True)
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