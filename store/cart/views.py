from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from cart.models import Cart
from cart.serializers import CartSerializer
from rest_framework import viewsets
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.response import Response
from product.models import Product
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def cart_quantity(request):
    quantity = 0
    carts = Cart.objects.all()
    for cart in carts:
        quantity = quantity + cart.quantity

    return HttpResponse(quantity)

def get_price_details(carts):
    sub_total = 0
    for cart in carts:
        sub_total = sub_total + cart.total
    delivery_charge = 0
    discount = 0
    total = 0
    if sub_total > 0:
        delivery_charge = 50
        discount = (5/100) * sub_total
        total = delivery_charge + (sub_total - discount)
    
    details = {
        "sub_total": sub_total,
        "delivery_charge": delivery_charge,
        "discount": discount,
        "total": total
    }
    return details

def get_cart_price_details(request):
    carts = Cart.objects.all()
    details = get_price_details(carts)
    return JsonResponse(details)

@csrf_exempt
def change_cart_quantity(request):
   try:
       carts = Cart.objects.all()
       cart_id = int(request.POST.get("cart_id"))
       new_quantity = int(request.POST.get("new_quantity"))
       cart_list = list(filter(lambda cart: cart.id == cart_id, carts))
       cart = cart_list[0]
       if cart is not None:
           cart.quantity = new_quantity
           cart.total = new_quantity * cart.product.pprice
           cart.save()
           return JsonResponse({'success': True})
       else: 
           return JsonResponse({'success': False})
   except:
       return JsonResponse({'success': False})


# Create your views here.
def cart(request): 
    carts = Cart.objects.all()
    # quantity = get_total_quantity_in_cart(carts)
    template = loader.get_template('cart.html')
    return HttpResponse(template.render({"carts":carts, "active_tab":"cart","request":request})) 

class DetailCart(DetailView):
    model = Cart
    template_name='cart/detail_cart.html'

class ListCart(ListView):
    model = Cart
    fields = "__all__"
    context_object_name = 'carts'
    template_name='cart.html'

class CreateCart(CreateView):
    model = Cart
    fields = "__all__"
    template_name = 'cart/create_cart.html'

class Updatecart(UpdateView):
    model = Cart
    template_name = 'cart/update_cart.html'

class DeleteCart(DeleteView):
    model = Cart
    template_name = 'cart/delete_cart.html'

def delete_cart(request, id, flag):
    cart = Cart.objects.get(id=id)
    cart.delete()
    if flag == 0:
        return redirect('/checkout/')
    else:
        return redirect('/cart/')

def add_to_cart(request, id, quantity):
    cart = Cart.objects.all()
    product = Product.objects.get(id=id)
    matching_products = list(filter(lambda d: d.product.id == id, cart))
    if len(matching_products) > 0:
        product_cart = matching_products[0]
        if product_cart is not None:
            product_quantity = product_cart.quantity + quantity
            total = product_quantity * product.pprice
            product_cart.total = total
            product_cart.quantity = product_quantity
            product_cart.save()

    else:
        total = quantity * product.pprice
        cart = Cart(product = product, quantity = int(quantity), total = total)
        cart.save()

    return redirect('/cart/')

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def create(self, request):
        print("new request")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200,data={"msg": "Item has been added to cart."})
        else:
           return Response(status=500,data={"msg": "Unable to add item to cart."})