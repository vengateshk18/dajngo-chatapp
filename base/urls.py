from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('home',views.home,name="home"),
    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),
    path('room/<str:pk>',views.room,name="room"),
    path('login/',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('register',views.register,name="register"),
    path('delete/<str:pk>/<str:rid>',views.delete_message,name="delete-message"),
    path('profile/<str:pk>',views.profile,name="profile"),
]