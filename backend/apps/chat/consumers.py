from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from chat.models import Conversation, Message


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """
 
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.conversation_name = None
        self.conversation = None
        self.user = None
 
    def connect(self):
        print("Connected!")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return
    
        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
        self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)
    
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )
 
    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)
 
    def receive_json(self, content, **kwargs):
        if content["type"] == "chat_message":
            message = Message.objects.create(
                from_user=self.user,
                to_user=self.get_receiver(),
                content=content["message"],
                conversation=self.conversation
            )
            async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "chat_message_echo",
                "name": content["name"],
                "message": content["message"],
            },
        )
        return super().receive_json(content, **kwargs)

    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)

    def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.username:
                # This is the receiver
                return get_user_model().objects.get(username=username)
