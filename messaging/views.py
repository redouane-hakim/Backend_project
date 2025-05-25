from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres import serializers
from rest_framework import generics, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from posts.models import Product
from django.db.models import Q, Count

User= get_user_model()
class StartConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        sender = request.user

        if sender.id == user_id:
            return Response({'detail': 'Cannot start a conversation with yourself.'}, status=400)

        try:
            receiver = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=404)

        # Check for existing 1-on-1 conversation (only 2 participants)
        existing_conversation = (
            Conversation.objects
            .filter(participants=sender)
            .filter(participants=receiver)
            .annotate(num_participants=Count('participants'))
            .filter(num_participants=2)
            .first()
        )

        if existing_conversation:
            return Response({'conversation_id': existing_conversation.id, 'created': False}, status=200)

        # Otherwise create a new one
        new_conversation = Conversation.objects.create()
        new_conversation.participants.add(sender, receiver)
        return Response({'conversation_id': new_conversation.id, 'created': True}, status=201)



class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user).order_by('-created_at')


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

class ConversationMessagesView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        conv_id = self.kwargs['conversation_id']

        try:
            conversation = Conversation.objects.get(id=conv_id)
        except Conversation.DoesNotExist:
            return Message.objects.none()

        if not conversation.has_participant(user):
            return Message.objects.none()

        return conversation.messages.all().order_by('timestamp')