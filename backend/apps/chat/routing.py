from django.urls import path
from chat.consumers import ChatConsumer

 
urlpatterns = [
    path("", ChatConsumer.as_asgi())
]
