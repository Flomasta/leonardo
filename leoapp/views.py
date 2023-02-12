from django.shortcuts import render
from .models import Items, PriceDynamic
from django.db.models import Q
import json
from datetime import date
import time


# Create your views here.

# def dashboard(request):
#     context = {}
#     return render(request, 'leoapp/index.html', context)


def dashboard(request, pk=1):
    pk = request.GET.get('pk', '')
    context = {}
    if pk:
        prices = PriceDynamic.objects.select_related('item_id').filter(Q(item_id__item_id=pk) | Q(item_id__title=pk))
        data = [[int(time.mktime(price.price_date.timetuple())), float(price.item_price)] for price in prices]
        json_data = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '))
        print(json_data)
        context = {'prices': prices, 'json_data': json_data}
    return render(request, f'leoapp/index.html', context)
    # pk = request.GET(pk, '')
    # prices = PriceDynamic.objects.select_related('item_id').filter(Q(item_id__item_id=pk) | Q(item_id__title=pk))
    # prices = Items.objects.all()
    # context = {'prices': prices, 'pk': pk}
    # return render(request, f'leoapp/index.html/{pk}', context)
