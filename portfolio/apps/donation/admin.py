from django.contrib import admin


from . models import Donation, Transaction

admin.site.register(Donation)
admin.site.register(Transaction)
