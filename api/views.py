from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from api.models import Conversation, SystemPrompt
from api.serializers import ConversationSerializer, SystemPromptSerializer
from api.chat_service.chatbot import get_message_from_chatbot
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.

# create CRUD API views here
class ConversationListCreate(generics.ListCreateAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

conversationSerializer_list_create = ConversationListCreate.as_view()

class ConversationRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

conversationSerializer_retrieve_update_destroy = ConversationRetrieveUpdateDestroy.as_view()

class SystemPromptListCreate(generics.ListCreateAPIView):
    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer

systemPromptSerializer_list_create = SystemPromptListCreate.as_view()

class SystemPromptRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = SystemPrompt.objects.all()
    serializer_class = SystemPromptSerializer

systemPromptSerializer_retrieve_update_destroy = SystemPromptRetrieveUpdateDestroy.as_view()

"""

class AnswerMessage(generics.GenericAPIView):
    serializer_class = []

    def post(self, request, *args, **kwargs):
        print('loi day')
        try:
            data = request.data
            conversation_id = data.get("conversation_id")
            message = data.get("message")
            output_ai_message = get_message_from_chatbot(conversation_id, message)
            return Response({"message": output_ai_message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "failed", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
answer_message = AnswerMessage.as_view()

"""
class AnswerMessage(generics.GenericAPIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["conversation_id", "message"],
            properties={
                "conversation_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                "message": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response("Successful response", schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            400: "Bad Request",
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            conversation_id = request.data.get("conversation_id")
            message = request.data.get("message")
            
            if not conversation_id or not message:
                return Response(
                    {"message": "conversation_id and message are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            output_ai_message = get_message_from_chatbot(conversation_id, message)
            return Response({"message": output_ai_message}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {"message": "failed", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

answer_message = AnswerMessage.as_view()
