from django.conf import settings
from django.db import models
from djstripe.models import Price, Product

from apps.utils.models import BaseModel


class Purchase(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    checkout_session_id = models.CharField(max_length=100, unique=True, db_index=True)
    is_valid = models.BooleanField(default=True)
