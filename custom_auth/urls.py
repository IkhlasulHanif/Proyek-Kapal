from django.urls import path
from .views import register, login_view, home, add_ship

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('add-ship/', add_ship, name='add_ship')
]