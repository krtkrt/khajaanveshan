from django.urls import path
from list.views import *
urlpatterns = [
    path('', login_view),
    path("logout/", logout_view),
    path("register/", register),
    path('index/', index),
    path('del/<str:item_id>', remove),
    path('edi/<int:id>', editindex),
]
