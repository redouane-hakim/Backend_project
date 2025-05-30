from django.contrib.auth import get_user_model
from django.contrib.postgres import serializers
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from posts.models import Product
from django.db.models import Q

User= get_user_model()
class StartConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):

        user=request.user

        target_user = User.objects.get(id=user_id)

        # Create a new conversation
        conversation = Conversation.objects.create(user1=user, user2=target_user)

        # Return the conversation ID or success message
        return Response({"conversation_id": conversation.id}, status=status.HTTP_201_CREATED)
class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.conversations.all()

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        product_id = self.request.data.get('product_reference')
        conversation = Conversation.objects.filter(id=conversation_id).first()
        if not conversation:
            raise serializers.ValidationError("Conversation not found.")
        if not conversation.has_participant(self.request.user):
            raise permissions.PermissionDenied("Not a participant in this conversation.")
        product = None
        if product_id:
            product = Product.objects.filter(id=product_id).first()
        serializer.save(sender=self.request.user, conversation=conversation, product_reference=product)

class StartConversationBuyProductView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        buyer = request.user
        seller = product.author
        # Check if conversation exists between buyer and seller
        conv = Conversation.objects.filter(participants=buyer).filter(participants=seller).first()
        if not conv:
            conv = Conversation.objects.create()
            conv.participants.add(buyer, seller)
        # Send initial message referencing product
        Message.objects.create(
            conversation=conv,
            sender=buyer,
            content=f"Interested in buying product: {product.id}",
            product_reference=product
        )
        return Response({"conversation_id": conv.id}, status=status.HTTP_201_CREATED)
