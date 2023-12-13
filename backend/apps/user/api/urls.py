from django.urls import path
from user.api.views import CustomObtainAuthTokenView


app_name = 'user_api'


urlpatterns = [
    path('auth-token/', CustomObtainAuthTokenView.as_view(), name='token'),
]