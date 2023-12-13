from django.urls import path
from chat.consumers import ChatConsumer

 
urlpatterns = [
    path("", ChatConsumer.as_asgi()),
    path("<conversation_name>/", ChatConsumer.as_asgi()),
]
