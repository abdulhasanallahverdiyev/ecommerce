from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	
	
	path('accounts/signup', views.signup, name="signup"),

	# chat
	# path('home/', views.home, name='home'),
    # path('<str:room>/', views.room, name='room'),
    # path('checkview', views.checkview, name='checkview'),
    # path('send', views.send, name='send'),
    # path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]
