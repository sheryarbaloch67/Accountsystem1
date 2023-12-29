from django.contrib import admin

# Register your models here.
from Accountapp.models import AccountingEntry, Head, claim, charge, paid, Vendor, Shead

admin.site.register(AccountingEntry)
admin.site.register(Head)
admin.site.register(Shead)
admin.site.register(paid)
admin.site.register(charge)
admin.site.register(claim)
admin.site.register(Vendor)
