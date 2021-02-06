from django.contrib import admin

# Register your models here.
from .models import CustomerAccount, Customer, Transactions

class TransactionsAdmin(admin.ModelAdmin):
    list_display = ["account", "action", "transactionamount", "currbalance", "created"]
    readonly_fields = ["account"]
    search_fields = ["account__customer__phone"]

class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name","phone","age","gender"]
    search_fields = ["phone"]

class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ["customer", "balance", "createdon", "lastmodified"]
    search_fields = ["customer__phone"]

admin.site.register(CustomerAccount, CustomerAccountAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Transactions, TransactionsAdmin)