from django.urls import path
from . import views

urlpatterns = [
    path('', views.concert_list, name='concert_list'),
    path('register/', views.register_user, name='register'), # Link daftar
    path('login/', views.login_user, name='login'),          # Link login
    path('logout/', views.logout_user, name='logout'),       # Link logout
    path('book/<int:concert_id>/', views.book_ticket, name='book_ticket'),
]