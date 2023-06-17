from django.db import models

class Currency(models.Model):
    name = models.CharField(max_length=255, null=False, default='')
    symbol = models.CharField(max_length=255, null=False, default='')
    status = models.CharField(max_length=255, null=False, default='ACTIVE')

    class Meta:
        db_table = 'currencies'

class Exchangerate(models.Model):

    start_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False, related_name='start_currency') 
    end_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=False,  related_name='end_currency')
    rate = models.FloatField(null=False, default=1)
    created_at = models.DateTimeField(null=True)

    class Meta:
        db_table = 'exchange_currency_rates'

class ExchangerateHistory(models.Model):

    exchange_rate = models.ForeignKey(Exchangerate, on_delete=models.CASCADE, null=False)
    rate = models.FloatField(null=False, default=1)
    from_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    class Meta:
        db_table = 'exchange_currency_rate_histories'
