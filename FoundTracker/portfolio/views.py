from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from .models import AssetClass, Currency, Operation
from django.contrib import messages
from .lib.asset_processor import process_asset_data 

import logging
import traceback

logger = logging.getLogger(__name__)


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class MainDashboardView(View):
    def get(self, request):
        return render(request, "portfolio/main_dashboard.html")

    # def post(self, request):

    #     return render(request, "portfolio/main_dashboard.html")


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketView(View):

    def load_data(self, request) -> dict:

        if (request.GET.get('pocket_name') == None):
            pocket_name = request.session['pocket_name']
        else:
            pocket_name = request.GET.get('pocket_name')
            request.session['pocket_name'] = pocket_name

        asset_classes = AssetClass.objects.all()
        currencies = Currency.objects.all()
        operations = Operation.objects.filter(owner=request.user)

        context = {
            'asset_classes': asset_classes,
            'currencies': currencies,
            'pocket_name': pocket_name,
            'operations': operations
        }

        return context

    def get(self, request):
        context = self.load_data(request)
        return render(request, "portfolio/pocket.html", context)

    def post(self, request):

        data = {
            'operation_type': request.POST['operation'],
            'ticker': request.POST['ticker'],
            'date': request.POST['date'],
            'currency': request.POST['currency'],
            'quantity': request.POST['quantity'],
            'price': request.POST['price'],
            'fee': request.POST['fee'],
            'comment': request.POST['comment'],
            'asset_class': request.POST['asset_class'],
            'owner': request.user,
            'pocket_name': request.session['pocket_name']
        }

        if data['fee'] == '':
            data['fee'] = '0'

        Operation.objects.create(
            operation_type=data['operation_type'],
            asset_class=data['asset_class'],
            ticker=data['ticker'],
            date=data['date'],
            currency=data['currency'],
            quantity=data['quantity'],
            price=data['price'],
            fee=data['fee'],
            comment=data['comment'],
            owner=data['owner']
        )

        try:
            _ = process_asset_data(data)
            messages.success(request, "Purchase added successfully")
        
        except Exception as error:
            logger.error("Purchase added error: {}".format(error))
            logger.error(traceback.format_exc()) 
            messages.error(request, "Purchase added error: {}".format(error))
            

        context = self.load_data(request)

        return render(request, "portfolio/pocket.html", context)


@method_decorator(login_required(login_url='/authentication/login'), name='get')
class PocketHistoryView(View):
    def get(self, request):
        operations = Operation.objects.filter(owner=request.user)
        context = {
            'operations': operations
        }
        return render(request, "portfolio/pocket_history.html", context)
