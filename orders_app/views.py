from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from .forms import CreateOrderForm
from .models import OrderModel
from users_app.models import BasketModel, CustomUser
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from http import HTTPStatus
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateOrderView(CreateView):
    model = OrderModel
    form_class = CreateOrderForm
    template_name = 'orders_app/order-create.html'
    success_url = reverse_lazy('orders_app:create_order_url')
    context_object_name = 'form'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1OdyPVAs5NfXtxw43dBBGHOZ',
                    'quantity': 1,
                },
            ],
            mode='payment',
            metadata={'order_id': self.object.id},
            success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders_app:success_order_url')),
            cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders_app:cancel_order_url'))
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


class SuccessOrderView(TemplateView):
    template_name = 'orders_app/success.html'


class CancelOrderView(TemplateView):
    template_name = 'orders_app/cancel.html'


endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")
