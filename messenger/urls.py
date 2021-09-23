from django.conf.urls import url
from django.urls import path, re_path
from rest_framework import routers


from .views import MessageHistoryViewset

router = routers.SimpleRouter()
# router.register(r'send',MessageEntryViewset, basename='send_message')
router.register(r'history',MessageHistoryViewset, basename='message_history')

urlpatterns = router.urls

