from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from emails.RegisterAPIView import RegisterAPIView, LogoutView
from emails.views import test
from emails.rules import Rules
from emails.actions import Actions

urlpatterns = [
    path('test',
         test,
         name='test'),
        path('login/',
         TokenObtainPairView.as_view(),
         name='token_obtain'),
    path('token_refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
    path('register_user/',
         RegisterAPIView.as_view(),
         name='Register'),
    path('logout/',
         LogoutView.as_view(),
         name='Logout'),
    path('get_rules/',
         Rules.as_view(),
         name='rules'),
    path('actions/',
         Actions.as_view(),
         name='rules'),
   
]
