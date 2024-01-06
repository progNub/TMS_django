from django.urls import path, include
from accounts.views import registration_view, user_logout, user_login, authentication_view
from django.contrib.auth import urls


urlpatterns = [
    path('authentication', authentication_view, name='authentication'),
    path('registration', registration_view, name='registration'),
    path('logout', user_logout, name='logout'),
    path('login',user_login, name='login')
]
