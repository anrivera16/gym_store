from django.db import transaction
from djstripe.models import Price, Product
from stripe.api_resources.checkout.session import Session

from apps.users.models import CustomUser

from .models import Purchase


@transaction.atomic
def create_purchase_from_checkout_session(session: Session) -> Purchase:
    session_id = session.stripe_id
    client_reference_id = int(session.client_reference_id)
    user = CustomUser.objects.get(id=client_reference_id)
    try:
        return Purchase.objects.get(checkout_session_id=session_id)
    except Purchase.DoesNotExist:
        product = Product.objects.get(id=session.line_items.data[0].price.product)
        price = Price.objects.get(id=session.line_items.data[0].price.id)
        return Purchase.objects.create(
            user=user,
            product=product,
            price=price,
            checkout_session_id=session_id,
        )
