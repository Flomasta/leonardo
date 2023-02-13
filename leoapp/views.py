from django.shortcuts import render
from .models import Items, PriceDynamic
from django.db.models import Q
import json
from datetime import date
import time


# Create your views here.

def dashboard(request):
    pk = request.GET.get('pk', '')
    context = {}
    if pk:
        prices = PriceDynamic.objects.select_related('item_id').filter(Q(item_id__item_id=pk) | Q(item_id__title__icontains=pk))
        if not prices:
            message = f'There is no items related to {pk}'
            return render(request, f'leoapp/index.html', {'message': message})
        # *1000 means that js requires timestamp with 13 digits, we have only 10. We add 3 more zeroes.
        data = [[int(time.mktime(price.price_date.timetuple())) * 1000, float(price.item_price)] for price in prices]
        # get item data (description,images,ect.)
        item_data = prices[0].item_id
        if item_data.images != 'no images':
            image = item_data.images.split('//')[1]
        else:
            # mock if there is no image in db
            image = 't4.ftcdn.net/jpg/04/00/24/31/360_F_400243185_BOxON3h9avMUX10RsDkt3pJ8iQx72kS3.jpg'
        context = {'prices': prices, 'json_data': data, 'item_data': item_data, 'image': image}
    return render(request, f'leoapp/index.html', context)
