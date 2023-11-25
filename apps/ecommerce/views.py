from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from djstripe.models import Product

from apps.utils.billing import get_stripe_module
from apps.web.meta import absolute_url

from .helpers import create_purchase_from_checkout_session
from .models import Purchase


@login_required
def ecommerce_home(request):
    products = Product.objects.filter(active=True, id__in=settings.ACTIVE_ECOMMERCE_PRODUCT_IDS).select_related(
        "default_price"
    )
    return TemplateResponse(
        request,
        "ecommerce/ecommerce_home.html",
        {
            "active_tab": "ecommerce",
            "products": products,
        },
    )


@login_required
def purchase_product(request, product_id: str):
    product = get_object_or_404(Product, id=product_id)
    stripe = get_stripe_module()
    success_url = absolute_url(reverse("ecommerce:checkout_success", args=[product_id]))
    cancel_url = absolute_url(reverse("ecommerce:checkout_cancelled", args=[product_id]))
    checkout_session = stripe.checkout.Session.create(
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
        customer_email=request.user.email,
        payment_method_types=["card"],
        client_reference_id=request.user.id,
        mode="payment" if not product.default_price.recurring else "subscription",
        line_items=[
            {
                "price": product.default_price.id,
                "quantity": 1,
            },
        ],
        allow_promotion_codes=True,
        metadata={
            "source": "ecommerce",  # used by the webhook to only process checkouts from here
        },
    )
    return HttpResponseRedirect(checkout_session.url)


@login_required
def checkout_success(request, product_id: str):
    # handle fulfillment
    product = get_object_or_404(Product, id=product_id)
    session_id = request.GET.get("session_id")
    session = get_stripe_module().checkout.Session.retrieve(session_id, expand=["line_items"])
    client_reference_id = int(session.client_reference_id)
    assert client_reference_id == request.user.id
    create_purchase_from_checkout_session(session)
    messages.success(
        request,
        _("Your purchase of {product_name} was successful. Thanks for the support!").format(product_name=product.name),
    )
    return HttpResponseRedirect(reverse("ecommerce:ecommerce_home"))


@login_required
def checkout_cancelled(request, product_id: str):
    product = get_object_or_404(Product, id=product_id)
    messages.info(request, _("Your purchase of {product_name} was cancelled.").format(product_name=product.name))
    return HttpResponseRedirect(reverse("ecommerce:ecommerce_home"))


@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return TemplateResponse(
        request,
        "ecommerce/purchases.html",
        {
            "active_tab": "ecommerce",
            "purchases": purchases,
        },
    )
