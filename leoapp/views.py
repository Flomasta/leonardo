from django.shortcuts import render
from .models import Items, PriceDynamic


# Create your views here.

def dashboard(request):
    prices = PriceDynamic.objects.select_related('item_id').all()
    return render(request, 'index.html', {'prices': prices})
