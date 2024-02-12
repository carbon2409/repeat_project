from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic import UpdateView
from .forms import CreateOrderForm
from .models import OrderModel
from products_app.models import ProductsModel
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from http import HTTPStatus
import stripe
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


def stripe_checkout(order_object):
    basket_items = order_object.basket['product_items']
    line_items = []
    for item in basket_items:
        data = {
            'price': ProductsModel.objects.get(name=item['product_name']).stripe_price_id,
            'quantity': item['quantity']
        }
        line_items.append(data)
    checkout_session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        metadata={'order_id': order_object.id},
        success_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders_app:success_order_url')),
        cancel_url='{}{}'.format(settings.DOMAIN_NAME, reverse('orders_app:cancel_order_url'))
    )
    return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


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
        return stripe_checkout(order_object=self.object)


class UpdateOrderView(UpdateView):
    model = OrderModel
    form_class = CreateOrderForm
    template_name = 'orders_app/order-update.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse_lazy('orders_app:update_order_url', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        super().post(self, request, *args, **kwargs)
        return stripe_checkout(order_object=self.object)


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
        session = event['data']['object']
        # Fulfill the purchase...
        fulfill_order(session)
    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = session.metadata['order_id']
    order = OrderModel.objects.get(id=order_id)
    order.actions_after_payment()


class OrderListView(ListView):
    model = OrderModel
    template_name = 'orders_app/orders.html'
    context_object_name = 'orders_list'

    def get_queryset(self):
        queryset = OrderModel.objects.filter(user=self.request.user.id)
        return queryset


class OrderDetailView(DetailView):
    model = OrderModel
    template_name = 'orders_app/order.html'
    context_object_name = 'order'
