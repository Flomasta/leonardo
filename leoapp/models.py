from django.db import models


class Items(models.Model):
    item_id = models.CharField(max_length=255, primary_key=True, verbose_name='ID')
    title = models.CharField(max_length=255, verbose_name='Title')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price', null=True)
    item_url = models.URLField(verbose_name='URL', null=True)
    images = models.TextField(verbose_name='Images', null=True)
    description = models.TextField(verbose_name='Description', null=True)
    breadcrumbs = models.TextField(verbose_name='Breadcrumbs', null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Item'


class Properties(models.Model):
    property_name = models.CharField(max_length=255, verbose_name='Property', unique=True)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name = 'Properties'
        verbose_name_plural = 'Properties'


class ItemProperty(models.Model):
    property_value = models.CharField(max_length=255, verbose_name='Value', null=True)
    property_id = models.ForeignKey(Properties, on_delete=models.CASCADE, verbose_name='Property ID')
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name='Item ID')

    class Meta:
        unique_together = (("property_id", "item_id"),)
        verbose_name = 'Item property'
        verbose_name_plural = 'Item property'

    def __str__(self):
        return str(self.property_id)


class PriceDynamic(models.Model):
    item_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Price', null=True)
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE, verbose_name='Item ID')
    price_date = models.DateField(verbose_name='Date')

    def __str__(self):
        return str(self.price_date)

    class Meta:
        verbose_name = 'Price dynamic'
        verbose_name_plural = 'Price dynamic'
