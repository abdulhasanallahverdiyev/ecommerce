from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData,guestOrder
from django.contrib.auth.forms import UserCreationForm
from .forms import SignupForm
from django.contrib.auth import authenticate, login
def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)



def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	
	else:
		customer,order=guestOrder(request,data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
		order.save()
	if order.shipping == True:
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=data['shipping']['address'],
			city=data['shipping']['city'],
			state=data['shipping']['state'],
			zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)


# Chat app
# def home(request):
#     return render(request, 'store/home.html')

# def room(request, room):
#     username = request.GET.get('username')
#     room_details = Room.objects.get(name=room)
#     return render(request, 'store/room.html', {
#         'username': username,
#         'room': room,
#         'room_details': room_details
#     })

# def checkview(request):
#     room = request.POST['room_name']
#     username = request.POST['username']

#     if Room.objects.filter(name=room).exists():
#         return redirect('/'+room+'/?username='+username)
#     else:
#         new_room = Room.objects.create(name=room)
#         new_room.save()
#         return redirect('/'+room+'/?username='+username)

# def send(request):
#     message = request.POST['message']
#     username = request.POST['username']
#     room_id = request.POST['room_id']

#     new_message = Message.objects.create(value=message, user=username, room=room_id)
#     new_message.save()
#     return HttpResponse('Message sent successfully')

# def getMessages(request, room):
#     room_details = Room.objects.get(name=room)

#     messages = Message.objects.filter(room=room_details.id)
#     return JsonResponse({"messages":list(messages.values())})



# Signup

def signup(request):
	if request.method=='POST':
		form=SignupForm(request.POST)
		if form.is_valid():
			form.save()
			username=form.cleaned_data.get('username')
			pwd=form.cleaned_data.get('password1')
			user=authenticate(username=username,password=pwd)
			login(request,user)
			return redirect('store')
	form=SignupForm
	return render(request,'registration/signup.html',{'form':form})















