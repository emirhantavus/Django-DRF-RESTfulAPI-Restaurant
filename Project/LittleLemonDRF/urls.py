from django.urls import path 
from . import views 
  
urlpatterns = [ 
    #path('ratings', views.RatingsView.as_view()), 
    path('groups/manager/users',views.manager_view),
    path('groups/manager/users/<int:id>',views.delete_manager),
    path('groups/deliver-crew/users',views.delivery_crew_view),
    path('groups/deliver-crew/users/<int:id>',views.delete_deliver_crew),
    path('menu-items',views.menu_items),
    path('menu-items/<int:id>',views.single_menu_items),
    path('cart/menu-items',views.cart_menu_items),
    path('orders',views.get_orders),
    path('orders/<int:id>',views.delete_order),
] 