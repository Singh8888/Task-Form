from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData



def store(request):
    data = cartData(request)
    
    
    cartItem = data['cartItem']
    Product_data=Product.objects.all()
    
    context={
        'Product_data':Product_data,
        'cartItem':cartItem
    }
    return render(request,'store/store.html',context)

def cart(request):
    # import pdb;pdb.set_trace()
    
    data = cartData(request)
    
    item = data['item']
    order = data['order']
    cartItem = data['cartItem']
               
    context={
        'item':item,
        'order':order,
        'cartItem':cartItem
    }
    return render(request,'store/cart.html',context)

def checkout(request):
    
    data = cartData(request)
    
    item = data['item']
    order = data['order']
    cartItem = data['cartItem']
    print(len(item))
    context={
        'item':item,
        'order':order,
        'cartItem':cartItem,
       }
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    # import pdb;pdb.set_trace()
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    
    orderItem,created= OrderItem.objects.get_or_create(product=product,order=order)
    
    if action=="add":
        orderItem.quantity=orderItem.quantity+1
    elif action=="remove":
        orderItem.quantity=orderItem.quantity-1

    orderItem.save()
    
    if orderItem.quantity<=0:
        orderItem.delete()
        
    return JsonResponse("item was added", safe=False)

def processOrder(request):
    transactionId= datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
       
    else:
    #    customer, order = guestOrder(request,data)
        print('COOKIES:',request.COOKIES)
        name= data['userFormData']['name']
        email= data['userFormData']['email']
        
        customer,created = Customer.objects.get_or_create(
            email=email,
        )
        customer.name=name
        customer.save()
        
        order = Order.objects.create(
            customer = customer,
            complete = False,
        )
        
        item_data = cookieCart(request)
        item = item_data['item']
        
        for i in item:
            product = Product.objects.get(id=i['product']['id'])
            orderItem = OrderItem.objects.create(
                product = product,
                order = order,
                quantity = i['quantity']
                
        )
        
       
    total=data['userFormData']['total']
    
    if total == str(order.get_cart_total):
        
        order.complete=True
    order.save()
    
    order.transaction_id = transactionId
    if (order.shipping == True):
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                state=data['shippingInfo']['state'],
                zipcode=data['shippingInfo']['zipcode'],
               
                 
                
            )

    return JsonResponse("order is processing", safe=False)
        

    
       
       
            
        