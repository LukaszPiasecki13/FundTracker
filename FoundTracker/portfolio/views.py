from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import AssetClass, Currency, Purchase
from django.contrib import messages


# Create your views here.


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class MainDashboardView(View):
    def get(self, request):
        return render(request, "portfolio/main_dashboard.html", )


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        asset_classes = AssetClass.objects.all()
        currency = Currency.objects.all()
        self.context = {
            'asset_classes': asset_classes,
            'currencies': currency,
        }

    def get(self, request):

        return render(request, "portfolio/pocket.html", self.context)

    def post(self, request):
        operation = request.POST['operation']

        ticker = request.POST['ticker']
        date = request.POST['date']
        currency = request.POST['currency']
        quantity = request.POST['quantity']
        price = request.POST['price']
        fee = request.POST['fee']
        comment = request.POST['comment']
        asset_class = request.POST['asset_class']
        owner = request.user


        if fee == '':
            fee = 0

        Purchase.objects.create(
            asset_class=asset_class,
            ticker=ticker,
            date=date,
            currency=currency,
            quantity=quantity,
            price=price,
            fee=fee,
            comment=comment,
            owner=owner
        )
        messages.success(request, "Purchase added successfully")

        return render(request, "portfolio/pocket.html", self.context)

@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketHistoryView(View):
    def get(self, request):
        return render(request, "portfolio/pocket_history.html", )
