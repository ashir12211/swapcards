from django.urls import path

from . import views

urlpatterns = [

    path('',views.home, name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('sell_page/',views.sell_page, name='sell_page'),
    path('sell_view/',views.sell_view, name='sell_view'),
    path('listings/',views.listings, name='listings'),
    # path('admin/manage-cards/', views.admin_manage_cards, name='admin_manage_cards'),
    path('buy_page/', views.buy_page, name='buy_page'),
    path('buy/<int:card_id>/', views.buy_gift_card, name='buy_gift_card'),
    path('payment/<int:card_id>/', views.payment_page, name='payment_page'),  
    path('confirm/<int:card_id>/', views.confirm_purchase, name='confirm_purchase'), 
    path('purchase_details/<int:card_id>/', views.purchase_details, name='purchase_details'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),


    

     



]