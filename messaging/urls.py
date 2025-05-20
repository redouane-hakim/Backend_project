from django.urls import path
from .views import ConversationListView, MessageCreateView, StartConversationBuyProductView

app_name = 'messaging'

urlpatterns = [
    path('conversations/', ConversationListView.as_view(), name='conversations-list'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
    path('buy-product/<int:product_id>/', StartConversationBuyProductView.as_view(), name='buy-product'),
]
