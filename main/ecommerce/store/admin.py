from django.contrib import admin
from .models import *


class customerAdmin(admin.ModelAdmin):
    list_display=('id','user','name','email')
    
admin.site.register(Customer,customerAdmin)


class productAdmin(admin.ModelAdmin):
    list_display=('id','name','price','digital')
    
admin.site.register(Product,productAdmin)

class orderAdmin(admin.ModelAdmin):
    list_display=('id','customer','date_ordered','complete','transaction_id')
    
admin.site.register(Order,orderAdmin)

class orderItemAdmin(admin.ModelAdmin):
    list_display=('id','product','order','quantity','date_added')
    
admin.site.register(OrderItem,orderItemAdmin)

class shippingAdmin(admin.ModelAdmin):
    list_display=('id','customer','order','address','city','state','zipcode','date_added')
    
admin.site.register(ShippingAddress,shippingAdmin)

