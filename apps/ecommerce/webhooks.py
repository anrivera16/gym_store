import logging

from djstripe import webhooks as djstripe_hooks

from apps.utils.billing import get_stripe_module

from .helpers import create_purchase_from_checkout_session

log = logging.getLogger("gym_store.ecommerce")


@djstripe_hooks.handler("checkout.session.completed")
def checkout_session_completed(event, **kwargs):
    """
    This webhook is called when a customer makes a purchase via Stripe Checkout.

    We create a Purchase record for this, if it was in our list of purchased products.
    """
    session = event.data["object"]
    # only process things that are tagged by this app "ecommerce"
    if session["metadata"].get("source") == "ecommerce":
        # get it back because we need the line items
        session = get_stripe_module().checkout.Session.retrieve(session["id"], expand=["line_items"])
        create_purchase_from_checkout_session(session)
