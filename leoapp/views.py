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


def dashboard(request, pk=None):
    pk = request.GET.get('pk', '')
    context = {}
    if pk:
        prices = PriceDynamic.objects.select_related('item_id').filter(Q(item_id__item_id=pk) | Q(item_id__title=pk))
        if not prices:
            message = f'There is no items related to {pk}'
            return render(request, f'leoapp/index.html', {'message': message})
        data = [[int(time.mktime(price.price_date.timetuple())) * 1000, float(price.item_price)] for price in prices]
        print(data)
        item_data = prices[0].item_id
        if item_data.images != 'no images':
            image = item_data.images.split('//')[1]
        else:
            image = 't4.ftcdn.net/jpg/04/00/24/31/360_F_400243185_BOxON3h9avMUX10RsDkt3pJ8iQx72kS3.jpg'

        context = {'prices': prices, 'json_data': data, 'item_data': item_data, 'image': image}
    return render(request, f'leoapp/index.html', context)
