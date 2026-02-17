from django.urls import path
from . import views

urlpatterns = [
 path('',views.home,name='home'),
 path('login/',views.user_login,name='login'),
 path('register/',views.register,name='register'),
 path('turfs/',views.turf_list,name='turf_list'),
 path('book/<int:turf_id>/',views.book_turf,name='book_turf'),
]
