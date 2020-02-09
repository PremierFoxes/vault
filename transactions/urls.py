from django.urls import path
from . import views

urlpatterns = [
    path('create_account', views.create_account, name='create_account'),
    path('', views.index, name='index'),
    path('buy_ticket', views.buy_ticket, name='buy_ticket'),
    path('get_account_balance', views.get_account_balance, name='get_account_balance'),
    path('deposit_funds', views.deposit_funds, name='deposit_funds')
]