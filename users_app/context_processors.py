from .models import BasketModel


def basket(request):
    user = request.user
    return {'basket': BasketModel.objects.filter(user=user) if request.user.is_authenticated else None}
