from django.urls import path
# internals
from api.views import *
from rest_framework.authtoken import views

#  UserView, TokenView,

urlpatterns = [
    path('chat/', ChatView.as_view(), name='code-explain' ),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

]
