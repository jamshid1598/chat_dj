from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.chat.api.views import ConversationViewSet, MessageViewSet
from apps.user.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("conversations", ConversationViewSet, basename='Conversations')
router.register("users", UserViewSet, basename='Users')
router.register("messages", MessageViewSet, basename='messages')


app_name = "api"
urlpatterns = router.urls