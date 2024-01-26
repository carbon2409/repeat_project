from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from .forms import CreateOrderForm
from .models import OrderModel
from users_app.models import BasketModel, CustomUser

class CreateOrderView(CreateView):
    model = OrderModel
    form_class = CreateOrderForm
    template_name = 'orders_app/order-create.html'
    success_url = reverse_lazy('orders_app:success_order_url')
    context_object_name = 'form'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     request.POST._mutable = True
    #     user = CustomUser.objects.get(id=self.request.user.id)
    #     post_data = dict(request.POST)
    #     post_data['user_id'] = user.id
    #     form = CreateOrderForm(request.POST)
    #     if form.is_valid():
    #         data = form.cleaned_data
    #         OrderModel.objects.create(first_name=data['first_name'], last_name=data['last_name'],
    #                                   user_id=post_data['user_id'], email=data['email'], address=data['address'])
    #         return render(request, 'orders_app/success.html')
    #     else:
    #         return render(request, 'orders_app/order-create.html', context={'form': form})

class SuccessOrderView(TemplateView):
    template_name = 'orders_app/success.html'
