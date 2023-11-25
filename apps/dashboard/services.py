import datetime
from typing import Optional

from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.users.models import CustomUser


def get_user_signups(start: Optional[datetime.date] = None, end: Optional[datetime.date] = None):
    end = end or timezone.now()
    start = start or end - datetime.timedelta(days=90)
    data = (
        CustomUser.objects.filter(date_joined__gte=start, date_joined__lt=end)
        .annotate(date=TruncDate("date_joined"))
        .values("date")
        .annotate(count=Count("id"))
        .order_by("date")
    )
    return data
