import json
from .models import *

def cookieCart(request):
    
    try: 
        cart = json.loads(request.COOKIES['cart'])
        print("heyyy")
           
    except:
        print("heyyy2")
        cart = {}
                
    print("cart:",cart)
    item=[]
    order={'get_cart_total':0,'get_cart_item':0,'shipping':False}
    cartItem = order['get_cart_item']

    for j in cart:
        try:
            cartItem += cart[j]['quantity']
            
            product = Product.objects.get(id=j)
            
            total = cart[j]['quantity']*product.price
            order['get_cart_total']+=total
            order['get_cart_item']+= cart[j]['quantity']
            
        
            cart_item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[j]['quantity'],
                'getTotal':total
            }
            item.append(cart_item)
            
            if product.digital == False:
                order['shipping']= True
        except:
            pass
    return {"cartItem":cartItem, 'order':order, 'item':item}


def cartData(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        item=OrderItem.objects.filter(order=order).all()
        cartItem = order.get_cart_item
    else:
        cookieData = cookieCart(request)
        cartItem = cookieData['cartItem']
        item = cookieData['item']
        order = cookieData['order']
        
    return {"cartItem":cartItem, 'order':order, 'item':item}
    

# def guestOrder(request,data):
    
#     print('COOKIES:',request.COOKIES)
#     name= data['userFormData']['name']
#     email= data['userFormData']['email']
    
#     customer,created = Customer.objects.get_or_create(
#         email=email,
#     )
#     customer.name=name
#     customer.save()
    
#     order = Order.objects.create(
#         customer = customer,
#         complete = False,
#     )
    
#     item_data = cookieCart(request)
#     item = item_data['item']
    
#     for i in item:
#         product = Product.objects.get(id=i['product']['id'])
#         orderItem = OrderItem.objects.create(
#             product = product,
#             order = order,
#             quantity = i['quantity']
            
#         )
    
#     return customer,order